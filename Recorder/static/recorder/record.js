document.addEventListener('DOMContentLoaded', () => {
    setup();

});

function ConvertSeconds(s)
{
    var min = Math.floor(s/60);
    var sec = s%60;
    return nf(min, 2) + ":" + nf(sec, 2);
}

function setup()
{
    let time = 70;
    document.querySelector('#timer').innerHTML = ConvertSeconds(time);
    let counter = 0;
    function timeint()
    {
        counter++;
        document.querySelector('#timer').innerHTML = ConvertSeconds(time-counter);
    }
    setInterval(timeint, 1000);

}