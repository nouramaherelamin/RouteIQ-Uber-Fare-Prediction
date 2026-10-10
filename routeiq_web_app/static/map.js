(() => {
  const $ = (id) => document.getElementById(id);
  const form = $('tripForm'), errorBox = $('errorBox'), estimateButton = $('estimateButton');
  const fields = ['pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude'];
  const defaultCoords = {pickup:[40.7580,-73.9855], drop:[40.7306,-73.9352]};
  const bounds = L.latLngBounds([[40.49,-74.28],[40.92,-73.68]]);
  const map = L.map('map', {zoomControl:false, scrollWheelZoom:true, preferCanvas:true}).setView([40.7484,-73.9857], 12);
  L.control.zoom({position:'bottomright'}).addTo(map);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom:19, attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a>'
  }).addTo(map);
  let selectionMode = null, routeRequest = 0, reverseRequest = {pickup:0,dropoff:0};
  const icons = {
    pickup:L.divIcon({className:'',html:'<div class="custom-pin pick"><span></span></div>',iconSize:[22,26],iconAnchor:[11,24]}),
    dropoff:L.divIcon({className:'',html:'<div class="custom-pin drop"><span></span></div>',iconSize:[22,26],iconAnchor:[11,24]})
  };
  const markers = {
    pickup:L.marker(defaultCoords.pickup,{icon:icons.pickup,draggable:true,title:'Pickup location'}).addTo(map),
    dropoff:L.marker(defaultCoords.drop,{icon:icons.dropoff,draggable:true,title:'Drop-off location'}).addTo(map)
  };
  let routeLine = L.polyline([defaultCoords.pickup,defaultCoords.drop],{color:'#8fffc5',weight:4,opacity:.92,dashArray:'8 7',lineCap:'round'}).addTo(map);
  const within = ([lat,lon]) => lat>=40.49 && lat<=40.92 && lon>=-74.28 && lon<=-73.68;
  const getCoord = (key) => [Number($(`${key}_latitude`).value),Number($(`${key}_longitude`).value)];
  const setCoord = (key, latlng) => {
    $(`${key}_latitude`).value = Number(latlng.lat).toFixed(6);
    $(`${key}_longitude`).value = Number(latlng.lng).toFixed(6);
    markers[key].setLatLng(latlng);
    updateRoute(); updateStats();
    reverseGeocode(key,latlng);
  };
  function updateStats(){
    const a=getCoord('pickup'), b=getCoord('dropoff');
    if (![...a,...b].every(Number.isFinite)) return;
    const R=6371.0088, rad=n=>n*Math.PI/180;
    const dlat=rad(b[0]-a[0]), dlon=rad(b[1]-a[1]);
    const h=Math.sin(dlat/2)**2+Math.cos(rad(a[0]))*Math.cos(rad(b[0]))*Math.sin(dlon/2)**2;
    const km=2*R*Math.asin(Math.min(1,Math.sqrt(h)));
    const y=Math.sin(dlon)*Math.cos(rad(b[0]));
    const x=Math.cos(rad(a[0]))*Math.sin(rad(b[0]))-Math.sin(rad(a[0]))*Math.cos(rad(b[0]))*Math.cos(dlon);
    const bearing=(Math.atan2(y,x)*180/Math.PI+360)%360;
    $('distanceLabel').textContent=km.toFixed(2)+' km'; $('summaryDistance').textContent=km.toFixed(2);
    $('bearingLabel').textContent=bearing.toFixed(0)+'°';
  }
  async function reverseGeocode(key,latlng){
    const req=++reverseRequest[key];
    const label=$(key==='pickup'?'pickupLabel':'dropLabel');
    label.value=`${latlng.lat.toFixed(5)}, ${latlng.lng.toFixed(5)}`;
    try{
      const url=`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(latlng.lat)}&lon=${encodeURIComponent(latlng.lng)}&zoom=16`;
      const response=await fetch(url,{headers:{'Accept':'application/json'}});
      if(!response.ok) return;
      const data=await response.json();
      if(req!==reverseRequest[key]) return;
      const addr=data.address||{};
      const place=addr.neighbourhood||addr.suburb||addr.road||addr.city_district||addr.city||data.name;
      if(place) label.value=place;
    }catch(_){/* Coordinates remain visible if reverse geocoding is unavailable. */}
  }
  async function updateRoute(){
    const requestId=++routeRequest, a=getCoord('pickup'), b=getCoord('dropoff');
    if(![...a,...b].every(Number.isFinite)) return;
    routeLine.setLatLngs([a,b]); routeLine.setStyle({color:'#8fffc5',dashArray:'8 7'});
    // Optional public OSRM demo routing: visual route only. The model uses direct geographic distance.
    try{
      const url=`https://router.project-osrm.org/route/v1/driving/${a[1]},${a[0]};${b[1]},${b[0]}?overview=full&geometries=geojson&steps=false`;
      const response=await fetch(url);
      if(!response.ok) return;
      const data=await response.json();
      if(requestId!==routeRequest||!data.routes?.length) return;
      routeLine.setLatLngs(data.routes[0].geometry.coordinates.map(([lon,lat])=>[lat,lon]));
      routeLine.setStyle({color:'#69d9ef',dashArray:null});
      $('mapInstructionText').textContent='Road route shown when available; fare features use direct distance.';
    }catch(_){/* Fallback line is drawn between pickup and drop-off. */}
  }
  function mode(key){selectionMode=key; $('choosePickup').classList.toggle('active',key==='pickup'); $('chooseDrop').classList.toggle('active',key==='drop'); $('mapInstructionTitle').textContent=key==='pickup'?'Choose pickup location':'Choose drop-off location'; $('mapInstructionText').textContent='Click anywhere inside the NYC map to place the selected pin.'; $('mapHint').textContent=key==='pickup'?'Pickup selected: click the map to place the mint pin.':'Drop-off selected: click the map to place the cyan pin.'; map.getContainer().style.cursor='crosshair'; $('map').scrollIntoView({behavior:'smooth',block:'nearest'}); }
  $('choosePickup').addEventListener('click',()=>mode('pickup'));
  $('chooseDrop').addEventListener('click',()=>mode('dropoff'));
  map.on('click',e=>{
    if(!selectionMode) { $('mapToast').textContent='Choose FROM or TO first, then click the map.'; $('mapToast').hidden=false; setTimeout(()=>$('mapToast').hidden=true,2400); return; }
    const key=selectionMode; if(!within([e.latlng.lat,e.latlng.lng])) { $('mapToast').textContent='Please select a point inside the supported NYC area.'; $('mapToast').hidden=false; setTimeout(()=>$('mapToast').hidden=true,2400); return; }
    setCoord(key,e.latlng); selectionMode=null; $('choosePickup').classList.remove('active'); $('chooseDrop').classList.remove('active'); map.getContainer().style.cursor=''; $('mapInstructionTitle').textContent='Route updated'; $('mapInstructionText').textContent='Drag either pin or select another point to adjust the trip.'; $('mapHint').textContent='You can move the pins on the map or edit coordinates below.';
  });
  Object.entries(markers).forEach(([key,marker])=>marker.on('dragend',()=>{
    const ll=marker.getLatLng(); if(!within([ll.lat,ll.lng])) { marker.setLatLng(key==='pickup'?getCoord('pickup'):getCoord('dropoff')); return; }
    setCoord(key,ll);
  }));
  fields.forEach(id=>$(id).addEventListener('change',()=>{
    const key=id.startsWith('pickup')?'pickup':'dropoff', ll=getCoord(key);
    if(!ll.every(Number.isFinite)||!within(ll)){ $(id).setCustomValidity('Coordinates must be inside the supported NYC area.'); $(id).reportValidity(); $(id).setCustomValidity(''); return; }
    markers[key].setLatLng(ll); reverseGeocode(key,L.latLng(ll[0],ll[1])); updateRoute(); updateStats(); map.panTo(ll);
  }));
  $('resetMap').addEventListener('click',()=>{
    setCoord('pickup',L.latLng(...defaultCoords.pickup)); setCoord('dropoff',L.latLng(...defaultCoords.drop)); map.fitBounds(L.latLngBounds(defaultCoords.pickup,defaultCoords.drop).pad(.8));
    $('pickupLabel').value='Times Square, Manhattan'; $('dropLabel').value='Flatiron District, Manhattan'; $('mapInstructionTitle').textContent='Choose your route'; $('mapInstructionText').textContent='Use the pins or click the map to set locations.';
  });
  form.addEventListener('submit',async event=>{
    event.preventDefault(); errorBox.hidden=true; estimateButton.disabled=true; estimateButton.innerHTML='<span>Calculating fare…</span><span class="button-arrow">↻</span>';
    try{
      const response=await fetch('/api/predict',{method:'POST',body:new FormData(form),headers:{'Accept':'application/json'}});
      const data=await response.json(); if(!response.ok||!data.ok) throw new Error(data.error||'Prediction failed.');
      $('fareAmount').textContent='$'+Number(data.prediction).toFixed(2); $('resultStatus').textContent='PREDICTION COMPLETE'; $('fareCaption').textContent='Model estimate · not an official fare or booking price.'; $('clearResult').hidden=false;
      $('routeSummary').innerHTML=`${safeText($('pickupLabel').value)} <i>→</i> ${safeText($('dropLabel').value)}`;
      $('summaryDistance').textContent=data.distance; $('distanceLabel').textContent=data.distance+' km'; $('bearingLabel').textContent=data.bearing;
      $('fareResult').classList.add('has-result');
    }catch(error){errorBox.textContent=error.message;errorBox.hidden=false;}
    finally{estimateButton.disabled=false;estimateButton.innerHTML='<span>Estimate fare</span><span class="button-arrow">↗</span>';}
  });
  function safeText(text){return String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  $('clearResult').addEventListener('click',()=>{$('fareAmount').textContent='$—';$('resultStatus').textContent='READY TO ESTIMATE';$('fareCaption').textContent='Your model prediction will appear here after you submit the trip.';$('clearResult').hidden=true;$('fareResult').classList.remove('has-result');});
  setTimeout(()=>map.invalidateSize(),120); updateStats(); updateRoute();
  reverseGeocode('pickup',L.latLng(...defaultCoords.pickup)); reverseGeocode('dropoff',L.latLng(...defaultCoords.drop));
})();
