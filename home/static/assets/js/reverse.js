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
            // TODO : add logic for on success
            // // deconstructing graph_context and new data
            // graph_context = {
            //     ...graph_context,
            //     ...data.graph
            // }
            
            // // update graph
            // visualize() 
        }
        });
    })
  );