function getSimilarTerms() {
    console.log("Inside the Similar Terms Function");
    
    // load CSV data
    d3.csv(graph_src, function(data) {
        var cols = data["columns"];
        cols.shift();

        R = getSimilarRelTerms(data, cols);
        fillSimilarTerms(graph_context["name"], graph_context["base_term"], R[0], R[1]);
    });
}

function fillSimilarTerms(model, base, r1, r2) {
    // Filling model type
    $(`#reverse-form #id_model_type option[value=${model}]`).prop('selected', true)

    // Filling Base Term
    $("#reverse-form input[name=base_term]").val(base);

    // Filling Relative Term 1
    $("#reverse-form input[name=rel_term1]").val(r1);
    
    // Filling Relative Term 2
    $("#reverse-form input[name=rel_term2]").val(r2);
}

function getSimilarRelTerms(data, cols){
    // get the terms from the min diff slice
    var minSlice = data[`${minDiffSlice(data, cols)}`];
    temp = [];
    for (var j=0; j<cols.length; j++){
        temp.push(minSlice[cols[j]]);
    }

    var posR = []
    posR = minDiffPairIndex(temp);

    return [cols[posR[0]], cols[posR[1]]];
}

function minDiffSlice(data, cols) {
    var lowestSlice = data.length;
    var sliceDiff = Infinity;
    
    // loop through all slices to find the slice with lowest diff
    for (var i=0; i<data.length; i++){
        slice = data[`${i}`];
        temp = [];
        for (var j=0; j<cols.length; j++){
            temp.push(slice[cols[j]]);
        }
        tempDiff = getMinDiff(temp)

        if (tempDiff <= sliceDiff) {
            sliceDiff = tempDiff;
            lowestSlice = i;
        }
    }

    return lowestSlice
}

function getMinDiff(arr){
    var smallestDiff=Infinity;
    copy = [...arr];
    arr.sort();

    /*Find pairs whose difference is minimum */
    for(var i=0 ; i < arr.length-1 ;i++){
        diff = Math.abs((arr[i]-arr[i+1]));
        if (diff <= smallestDiff) smallestDiff=diff;
    }

    return smallestDiff;
}

function minDiffPairIndex(arr){
    var smallestDiff=Infinity;
    copy = [...arr];
    arr.sort(),
    smallA = -1
    smallB = -1

    /*Find pairs whose difference is minimum */
    for(var i=0 ; i < arr.length-1 ;i++){
        diff = Math.abs((arr[i]-arr[i+1]));
        
        if (diff <= smallestDiff) {
            smallestDiff=diff;
            smallA = arr[i];
            smallB = arr[i+1];
        }
    }
    
    const idxA = copy.indexOf(smallA);
    const idxB = copy.indexOf(smallB);

    return [idxA, idxB];
};

$(document).ready(
    $('#revFormFill').click( function () {
        getSimilarTerms();
    })
);