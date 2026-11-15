// Visitor statistics (GoatCounter, free and cookie-free).
// To switch on: create a free account at https://www.goatcounter.com, then put the site code below,
// e.g. var GOATCOUNTER_CODE = 'agentiq';  Leave it empty to keep statistics off.
var GOATCOUNTER_CODE = '';

(function(){
  if (!GOATCOUNTER_CODE) return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  s.setAttribute('data-goatcounter', 'https://' + GOATCOUNTER_CODE + '.goatcounter.com/count');
  document.head.appendChild(s);
})();
