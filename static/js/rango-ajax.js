$(document).ready(function() {
    $('.like_btn').click(function() {
        var reviewIdVar;
        reviewIdVar = $(this).attr('data-reviewid');

        $.get('/like_review/',
            {'review_id': reviewIdVar},
            function(data) {
                $('#like_count'+reviewIdVar).html(data);
                $('#like_btn'+reviewIdVar).hide();
            })
    });

    $('.dislike_btn').click(function() {
        var reviewIdVar;
        reviewIdVar = $(this).attr('data-reviewid');

        $.get('/dislike_review/',
            {'review_id': reviewIdVar},
            function(data) {
                $('#like_count'+reviewIdVar).html(data);
                $('#dislike_btn'+reviewIdVar).hide();
            })
    });

});