$(document).ready(
    $('#graph-form').submit(function(e){
        console.log("graph form submit!!!");
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
        type:"POST",
        url: "/graph_update/",
        data:  serializedData,

        success: function(data){
            // deconstructing graph_context and new data
            graph_context = {
                ...graph_context,
                ...data.graph
            }
            
            // update graph
            visualize() 
        }
    });
}));

// TODO: see why this is not working
$(window).resize(regraph);

function regraph() {
    console.warn("regraph!!");
    visualize();
}