function update_carousel() {
    // buttons and texts
    const prevButton = $("#prevButton")[0];
    const nextButton = $("#nextButton")[0];
    const texts = reverse_context['docs'];

    // slide id 
    var id = 0;

    // set original slide for on load
    showSlide(id);

    /**
     * prevButton() -> decremenets id
     */
    prevButton.addEventListener("click", () => {
        console.log("prev click");
        id == 0 ? id = texts.length-1 : id -= 1
        showSlide(id);
    });

    /**
     * nextButton() -> increments id
     */
    nextButton.addEventListener("click", () => {
        console.log("next click");
        id == texts.length-1 ? id = 0 : id += 1
        showSlide(id);
    });

    /**
     * showSlide() -> shows slide at given id (array index)
     * @param {Integer} id 
     */
    function showSlide (id) {
        $("#slideContent").empty();
        const header = $("<h3>Title</h3>");
        const text = $(`<p>${highlight(texts[id][0], texts[id][1])}</p>`);
        $("#slideContent").append(header);
        $("#slideContent").append(text);
    }

    /**
     * highlight: highlights given text
     * if base: highlight yellow
     * if not: highlight blue
     * @param {String} text 
     * @param {Integer[]} locs 
     */
    function highlight(text, locs) {
        var tokens_list = text.split(" ");
        for (let i = 0; i < locs.length; i++) {
            if (i==0) {
                tokens_list[locs[i]] = `<span class=\"highlightBase\">${tokens_list[locs[i]]}</span>`;
            } else {
                if (locs[i]!=-1) {
                    tokens_list[locs[i]] = `<span class=\"highlightRel\">${tokens_list[locs[i]]}</span>`;
                }
            }    
        }
        return tokens_list.join(" ");
    }
};