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
            console.log("reverse form Ajax Success");


            // reverse_context['docs'] = data['text'];

            // deconstructing reverse_context and updating with new data
            console.log(data);
            console.log(reverse_context);

            // // nyt data (base: race), (rel_terms: ['state', 'government'])
            // reverse_context = {
            //     code: 200,
            //     revData: {
            //         base: data.base,
            //         rel1: data.rel_terms[0],
            //         rel2: data.rel_terms[1],
            //         docs: Array[data.text]
            //     }
            // }

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
    console.warn("reCarousel 2!!");
    update_carousel()
}

window.onresize = reCarousel;
