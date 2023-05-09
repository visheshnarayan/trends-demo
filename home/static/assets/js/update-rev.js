$(document).ready(
    $('#reverse-form').submit(function(e){
        console.log("reverse form submit!!!");

        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
        type:"POST",
        url: "/reverse/",
        data:  serializedData,

        success: function(data){

            // TODO : also should think about what to do if there is no text with both words 
            
            // reverse_context['docs'] = data['text'];

            // deconstructing reverse_context and updating with new data
            // console.log(data);
            // console.log(reverse_context);

            reverse_context = {
                ...reverse_context,
                ...data.revData
            }
            
            // update carosel
            update_carousel()
        },

        error: function(data) {
            console.error("reverse form Ajax Failed");
        }
    });
}));

// TODO : make Carousel responsive
function reCarousel() {
    update_carousel()
}

window.onresize = reCarousel;
