$(document).ready(
    $('#graph-form').submit(function(e){
        console.log("form submit!!!");
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
        type:"POST",
        url: "/graph_update/",
        data:  serializedData,

        success: function(data){
            // console.log(data);

            // console.log("graph context data : ", graph_context);

            // deconstructing graph_context and new data
            graph_context = {
                ...graph_context,
                ...data.graph
            }

            // console.log("new graph context data : ", graph_context);
            
            // update graph
            visualize() 
        }
        });
    })
  );