function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
$('#wow1').attr('aria-valuenow', normal_pork).css('width', normal_pork);
$('#wow2').attr('aria-valuenow', beta_pork).css('width', beta_pork);
$('#wow3').attr('aria-valuenow', parasite_pork).css('width', parasite_pork);
