$(document).ready(
    $('#graph-form').submit(function(e){
        console.log("form submit");
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
        type:"POST",
        url: "/graph_update/",
        data:  serializedData,

        //   TODO : Add error hanling
        success: function(data){
            console.log(data);

            // TODO : update other terms as well (other than base and rel terms)
            graph_context

            console.log("graph context data : ", graph_context);
            graph_context["base_term"] = data["base_term"];
            graph_context["rel_terms"] = data["rel_terms"];
            console.log("new graph context data : ", graph_context);
            // $("#result").text(data["result"]);
            // update graph
            visualize() 
        }
        });
    })
  );