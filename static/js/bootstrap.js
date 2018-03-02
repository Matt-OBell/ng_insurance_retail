// A $( document ).ready() block.
$( document ).ready(function() {
    var allReadMore = document.querySelectorAll('a[typ="btn"]');
    allReadMore.forEach(function(readyMore){
      readyMore.addEventListener('click', function(){
        var tid = readyMore.getAttribute('tid');
        readyMore.style.display = 'none';
        var more = document.querySelector(`span[class="${tid}"]`);
        more.style.display = 'block';
      });
    });

    //
    var allLess = document.querySelectorAll('a[typ="less"]');
    allLess.forEach(function(readyLess){
      readyLess.addEventListener('click', function(){
        var tid = readyLess.getAttribute('tid');
        readyLess.style.display = 'none';
        var less = document.querySelector(`span[class="${tid}"]`);
        less.style.display = 'block';
      });
    });
});