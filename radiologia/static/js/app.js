
$( document ).ready(function() {
    console.log( "ready!" )

    acconsento = Cookies.get('privacy')
    console.log(Cookies.get())

    if (acconsento == 'true') {
        $(".footer").hide();
    }


    $("#acconsento").click(function() {
        $(".footer").hide();
        Cookies.set('privacy', 'true');
    })

    if ($('#instructions') && $('#instructions').is(":visible")) {
        $(document).scrollTop( $("#instructions").offset().top )
    } else {
        console.log($('#instructions'))
    }


    /*$('#languagepicker').on("change", function() {
        console.log('changed language: '+this.value)
        $.ajax({
            type: "POST",
            url: "index/language",
            data: {"lang" : this.value},
            success: function(data) {
                console.log(data)
                location.reload()
            }
          })
    })*/

})