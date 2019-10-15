function popup(){
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

// POP OVER Kram
  $(function() {
         var timer = null;
         var xhr = null;
         $('.bg_popup').hover(
             function(event) {
                 // mouse in event handler
                 var elem = $(event.currentTarget);
                 timer = setTimeout(function() {
                     timer = null;
                     xhr = $.ajax(
                         '/boardgame/'+ elem.text().trim().split("-")[0].trim() +'/popup').done( //' + elem.first().text().trim() + '
                           function(data) {
                               xhr = null;
                               elem.popover({
                                   trigger: 'manual',
                                   html: true,
                                   animation: false,
                                   container: elem,
                                   content: data
                               }).popover('show');
                               flask_moment_render_all();
                           }
                         );
                 }, 1000);
             },
             function(event) {
                // mouse out event handler
                var elem = $(event.currentTarget);
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                else if (xhr) {
                    xhr.abort();
                    xhr = null;
                }
                else {
                    elem.popover('destroy');
                }
            }
         )
     });
