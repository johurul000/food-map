$(document).ready(function() {
    var suggestionsBox = $('#suggestions')
    $('#search-box').on('input', function() {
        var query = $(this).val()
        if (query.length > 2) {
            $.ajax({
                url: searchSuggestionsUrl,
                data: { 'query': query },
                success: function(data) {
                    suggestionsBox.empty()
                    if (data.length > 0) {
                        data.forEach(function(item) {
                            suggestionsBox.append('<div class="suggestion-item">' + item.name + ' - ' + item.restaurant + '</div>')
                        })
                        suggestionsBox.show()
                    } else {
                        suggestionsBox.hide()
                    }
                }
            })
        } else {
            suggestionsBox.hide()
        }
    })

    $(document).on('click', '.suggestion-item', function() {
        $('#search-box').val($(this).text())
        suggestionsBox.hide()
    })

    
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#suggestions').length && !$(event.target).is('#search-box')) {
            suggestionsBox.hide()
        }
    })
})
