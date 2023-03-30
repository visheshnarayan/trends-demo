function update_carousel(){
    console.log("inside carousel function");
    console.warn(reverse_context);

    //reverse_context -> data 
    // TODO: write jquery to update carousel 
    // TODO: refactor with jquery
    // TODO: style the slides so they look correct
    const texts = reverse_context['docs'];
    texts.forEach(text => {
        /**
         * initialize list first and set it equal to "first-slide" incase indexOf == 0 else create new li
         * --> this is done so the "data-active" meta-tag is assigned to the first text inserted and so the preview is not blank on load 
         * every other node created and joined the same way
         */
        
        // get initial list item if first text
        var list
        texts.indexOf(text) == 0 ? list = $("#first-slide") : list = $("<li></li>", {"class": "slides"}).appendTo("slides");

        /**
         * create element nodes
         */
        const div = $("<div></div>", {"class": "content"});
        const header = $("<h3>Title</h3>")
        const p = $(`<p>${text}</p>`)
    
        /**
         * append all nodes
         */
        div.append(header)
        div.append(p)
        list.append(div)
        $("#slides").append(list)
    })
};