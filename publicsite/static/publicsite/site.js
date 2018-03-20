// console.log('jQuery loaded.');
$(document).ready(function(){
  // console.log('ready');
  // console.log(location.pathname.split("/")[1]);
  if(location.pathname != "/") {
    $('.nav a[href^="/' + location.pathname.split("/")[1] + '/"]').parent().addClass('active');
  } else $('.nav a:eq(0)').parent().addClass('active');
  $(document).click(function (event) {
    var clickover = $(event.target);
    var _opened = $(".navbar-collapse").hasClass("in");
    if (_opened === true && !clickover.hasClass("navbar-toggle")) {
        $("button.navbar-toggle").click();
    }
  });
  $('li').click(function() {
    if (!$(this).hasClass("active")) {
    $("li.active").removeClass("active");
    $(this).addClass("active");
  }});
});