$('#graph-form .basicAutoComplete').autoComplete({
    resolver: 'custom',
    events: {
        search: function (qry, callback) {
            urlink = '/term_autocomplete/' + $('#id_model_type').find(":selected").val() + '/';
            // let's do a custom ajax call
            $.ajax(
                urlink,
                {
                    data: {'q': qry}
                }
            ).done(function (res) {
                callback(res)
            });
        }
    },
    minLength: 1,
});

$('#reverse-form .basicAutoComplete').autoComplete({
    resolver: 'custom',
    events: {
        search: function (qry, callback) {
            urlink = '/term_autocomplete/' + $('#reverse-form #id_model_type').find(":selected").val() + '/';
            // let's do a custom ajax call
            $.ajax(
                urlink,
                {
                    data: {'q': qry}
                }
            ).done(function (res) {
                callback(res)
            });
        }
    },
    minLength: 1,
});