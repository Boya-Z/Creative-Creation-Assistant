

  var dr = document.referrer
  var ttdRef = encodeURIComponent( dr );
  var ttdNobounce = ""
  if ( dr ){
    var referrer = new URL( dr );
    if (referrer.hostname === window.location.hostname) {
      var searchParams = new URLSearchParams(referrer.search);
      for (let [key, value] of searchParams.entries()) {
        if ( key.includes('utm_') ){
	      ttdNobounce = "no_bounce"
	    }
      }
    }
  }
  ttd_dom_ready( function() {
    if (typeof TTDUniversalPixelApi === 'function') {
      var universalPixelApi = new TTDUniversalPixelApi();
      universalPixelApi.init("akd8pws", ["t7ssy6x"], "https://insight.adsrvr.org/track/up", {td1: ttdRef, td2:ttdNobounce});
    }
  });