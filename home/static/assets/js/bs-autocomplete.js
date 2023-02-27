$('.basicAutoComplete').autoComplete({
    resolverSettings: {
        url: '/term_autocomplete/' + $('#id_model_type').find(":selected").val() + '/'
    },
    minLength: 1,
});