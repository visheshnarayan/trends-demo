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
        var list

        // new
        texts.indexOf(text) == 0 ? list = $("#first-slide") : list = $("<li></li>", {"class": "slides"}).appendTo("slides");
        // list.addClass("slide");
        // var $div = $("<div>", {id: "foo", "class": "a"});
        // if (texts.indexOf(text) == 0) {list = $("#first-slide")} else {list = $("div", {"class": "slide"})}
    
        /**
         * create element nodes
         */
        const div = $("<div></div>", {"class": "content"})
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

    /**
     * left and right buttons
     */
    const buttons = document.querySelectorAll("[data-carousel-button]")

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            // go right if "next" button: go left if not
            const offSet = button.dataset.carouselButton === "next" ? 1 : -1

            // go into data-carousel and select data-slides
            const slides = button
                .closest("[data-carousel]")
                .querySelector("[data-slides]")

            const activeSlide = slides.querySelector(["[data-active]"])

            // index of active slide + offset
            let newIndex = [...slides.children].indexOf(activeSlide) + offSet

            // if first send to last slide
            if (newIndex < 0) newIndex = slides.children.length - 1

            // if index greater than length send to first slide
            if (newIndex >= slides.children.length) newIndex = 0

            // new active slide
            slides.children[newIndex].dataset.active = true

            // delete old active slide
            delete activeSlide.dataset.active
        })
    })
};