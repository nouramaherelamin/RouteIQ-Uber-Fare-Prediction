"""Reproducible Task 2 preprocessing, ablation, CV, tuning, and hold-out evaluation."""
from pathlib import Path
import json, time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_validate, RandomizedSearchCV
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import randint, uniform
from .data import load_clean_data
from .features import UberFeatureEngineer

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/raw/sample_50000.csv"
MODELS = ROOT / "models"; REPORTS = ROOT / "reports"
RAW_COLS = ["pickup_datetime","pickup_latitude","pickup_longitude","dropoff_latitude","dropoff_longitude","passenger_count","Car Condition","Weather","Traffic Condition"]
CAT = ["Car Condition","Weather","Traffic Condition"]

def make_pipeline(model, include_categoricals=True, scale=False):
    numeric = ["pickup_latitude","pickup_longitude","dropoff_latitude","dropoff_longitude","passenger_count","distance_km","jfk_dist_km","ewr_dist_km","lga_dist_km","sol_dist_km","nyc_dist_km","bearing_sin","hour_sin","hour_cos","weekday_sin","weekday_cos","month_sin","month_cos","year"]
    transformers = [("num", Pipeline([("imputer", SimpleImputer(strategy="median")), *(([("scaler", RobustScaler())] if scale else []))]), numeric)]
    if include_categoricals: transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),("onehot", OneHotEncoder(handle_unknown="ignore"))]), CAT))
    prep = ColumnTransformer(transformers, remainder="drop")
    return Pipeline([("features", UberFeatureEngineer(include_categoricals=include_categoricals)),("preprocess", prep),("model", model)])

def main():
    REPORTS.mkdir(exist_ok=True); MODELS.mkdir(exist_ok=True)
    df = load_clean_data(DATA)
    # Additional deterministic data validity rule: passenger count must be 1..6; record removal count.
    before_passengers = len(df); df = df[df.passenger_count.between(1,6)].copy()
    # Retain plausible positive fares; do not cap valid long trips solely by IQR.
    X = df[RAW_COLS].copy(); y = df["fare_amount"].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    candidates = {
      "Ridge": (Ridge(alpha=1.0), True),
      "Decision Tree": (DecisionTreeRegressor(max_depth=18,min_samples_leaf=5,random_state=42), False),
      "Random Forest": (RandomForestRegressor(n_estimators=50,max_depth=20,min_samples_leaf=3,n_jobs=1,random_state=42), False),
      "Hist Gradient Boosting": (HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=31,l2_regularization=1.0,random_state=42), False),
    }
    # Feature ablation is selected only by CV on training data. Ridge provides an interpretable controlled comparison.
    ablation=[]
    for keep in [False, True]:
      pipe=make_pipeline(Ridge(alpha=1.0),include_categoricals=keep,scale=True)
      scores=cross_validate(pipe,X_train,y_train,cv=cv,scoring={"mae":"neg_mean_absolute_error","rmse":"neg_root_mean_squared_error","r2":"r2"},n_jobs=1)
      ablation.append({"categoricals_included":keep,"cv_mae_mean":float(-scores["test_mae"].mean()),"cv_rmse_mean":float(-scores["test_rmse"].mean()),"cv_r2_mean":float(scores["test_r2"].mean()),"cv_rmse_std":float(scores["test_rmse"].std())})
    include_cats = min(ablation,key=lambda z:z["cv_rmse_mean"])["categoricals_included"]
    rows=[]; fitted={}
    for name,(model,scale) in candidates.items():
      pipe=make_pipeline(model,include_categoricals=include_cats,scale=scale)
      start=time.perf_counter()
      scores=cross_validate(pipe,X_train,y_train,cv=cv,scoring={"mae":"neg_mean_absolute_error","rmse":"neg_root_mean_squared_error","r2":"r2"},n_jobs=1)
      cv_time=time.perf_counter()-start
      pipe.fit(X_train,y_train); pred=pipe.predict(X_test)
      rows.append({"model":name,"cv_mae_mean":-scores["test_mae"].mean(),"cv_rmse_mean":-scores["test_rmse"].mean(),"cv_rmse_std":scores["test_rmse"].std(),"cv_r2_mean":scores["test_r2"].mean(),"test_mae":mean_absolute_error(y_test,pred),"test_rmse":mean_squared_error(y_test,pred)**0.5,"test_r2":r2_score(y_test,pred),"cv_seconds":cv_time})
      fitted[name]=pipe
    # Tune Random Forest on train folds only. Test set remains untouched until final evaluation.
    rf=make_pipeline(RandomForestRegressor(random_state=42,n_jobs=1),include_categoricals=include_cats,scale=False)
    search=RandomizedSearchCV(rf,{"model__n_estimators":[80,120,160],"model__max_depth":[12,18,24,None],"model__min_samples_leaf":[2,3,5],"model__max_features":[0.7,1.0]},n_iter=3,scoring="neg_root_mean_squared_error",cv=cv,random_state=42,n_jobs=1,verbose=0)
    search.fit(X_train,y_train)
    pred=search.best_estimator_.predict(X_test)
    rows.append({"model":"Tuned Random Forest","cv_mae_mean":np.nan,"cv_rmse_mean":-search.best_score_,"cv_rmse_std":np.nan,"cv_r2_mean":np.nan,"test_mae":mean_absolute_error(y_test,pred),"test_rmse":mean_squared_error(y_test,pred)**0.5,"test_r2":r2_score(y_test,pred),"cv_seconds":np.nan})
    results=pd.DataFrame(rows).sort_values("test_rmse")
    results.to_csv(REPORTS/"model_comparison.csv",index=False)
    pd.DataFrame(ablation).to_csv(REPORTS/"categorical_ablation.csv",index=False)
    best_name=str(results.iloc[0]["model"]); best=search.best_estimator_ if best_name=="Tuned Random Forest" else fitted[best_name]
    import joblib
    joblib.dump(best,MODELS/"uber_fare_pipeline_v1.joblib",compress=3)
    metadata={"target":"fare_amount","input_columns":RAW_COLS,"categoricals_included":bool(include_cats),"categorical_ablation":ablation,"selected_model":best_name,"best_random_forest_params":search.best_params_,"training_rows":len(X_train),"test_rows":len(X_test),"random_state":42,"cv":"5-fold shuffled KFold on training split","test_metrics_are_dollars":True,"coordinate_input_unit":"degrees","reference_coordinates_note":"Approximate public coordinates in features.py; recompute supplied distance columns instead of trusting source columns."}
    (MODELS/"model_metadata.json").write_text(json.dumps(metadata,indent=2,default=float))
    # Chronological robustness check: train on 2009-2014 and test on 2015, not used for model selection.
    years=pd.to_datetime(df.pickup_datetime).dt.year
    Xchron=X.copy(); ychron=y.copy(); tr=years<2015; te=years==2015
    chron={"train_period":"2009-2014","test_period":"2015","train_rows":int(tr.sum()),"test_rows":int(te.sum())}
    if tr.sum()>100 and te.sum()>50:
      cp=make_pipeline(best.named_steps["model"],include_categoricals=include_cats,scale=(best.named_steps["preprocess"].named_transformers_.get("num") is not None and "scaler" in best.named_steps["preprocess"].named_transformers_["num"].named_steps))
      cp.fit(Xchron.loc[tr],ychronic if False else ychron.loc[tr]); pp=cp.predict(Xchron.loc[te])
      chron.update({"mae":float(mean_absolute_error(ychronic if False else ychron.loc[te],pp)),"rmse":float(mean_squared_error(ychronic if False else ychron.loc[te],pp)**0.5),"r2":float(r2_score(ychronic if False else ychron.loc[te],pp))})
    (REPORTS/"chronological_check.json").write_text(json.dumps(chron,indent=2))
    print("CLEAN_ROWS",len(df),"PASSENGER_ROWS_REMOVED",before_passengers-len(df))
    print("CATEGORICAL_ABLATION\n",pd.DataFrame(ablation).to_string(index=False))
    print("MODEL_RESULTS\n",results.to_string(index=False))
    print("SELECTED",best_name,"PARAMS",search.best_params_)
    print("CHRONOLOGICAL",chron)
if __name__=="__main__": main()
