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
            // TODO : also should think about what to do if there is no text with both words 
            // TODO : preset filled in words with displayed text anagolous to trends graph above 
            
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

// ,

//     $(function(){
//         $('#revFormFill').click(function() {
//             // TODO : add functionality to fill reverse form with the most similar terms from the above graph context
//             // alert("Hello");
            
//             texts.forEach(text => {
//                 /**
//                  * initialize list first and set it equal to "first-slide" incase indexOf == 0 else create new li
//                  * --> this is done so the "data-active" meta-tag is assigned to the first text inserted and so the preview is not blank on load 
//                  * every other node created and joined the same way
//                  */
//                 var list
//                 if (data.indexOf(text) == 0) {list = document.getElementById("first-slide")} else {list = document.createElement("li")}
            
//                 /**
//                  * create element nodes
//                  */
//                 list.className = "slide"
//                 const div = document.createElement("div")
//                 div.className = "content"
//                 const header = document.createElement("h3")
//                 const headerText = document.createTextNode("Title")
//                 const p = document.createElement("p")
//                 const pText = document.createTextNode(text)
            
//                 /**
//                  * append all nodes
//                  */
//                 p.appendChild(pText)
//                 header.appendChild(headerText)
//                 div.appendChild(header)
//                 div.appendChild(p)
//                 list.appendChild(div)
//                 document.getElementById("slides").appendChild(list)
//             })
//         });
//     })

// );