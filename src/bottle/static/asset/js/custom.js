$(document).ready(function() {
    var networkSel = document.getElementById("formNetworkSelect");

    networkSel.onchange = function() {
        $("#formTagsSelect").empty().append('<option value="" id="tagLoading" selected="selected">Please select network first</option>');;
        $.ajax({
            url: '/api/get_tags',
            type: "POST",
            data: {
                network_site: this.value,
                auth_key: 'f883af4981c6d.bcdb777cebe0ab5aa76,277ddca765f616c03a9c5629afcb5798!e1513'
            },
            success: function(data){

                $.each(data.result, function(key, modelName){
                    var option = new Option(modelName.text, modelName.value);
                    $("#formTagsSelect").append(option);
                });

                $('#tagLoading').text('Select site');

            }
        });
    }
});