var index = 0;
var questions;

$(function(){
	questions = $('.question');
	setQuestionSelf('.answer .item', nextQuestion);
	$(questions[index]).show();
});

function setQuestionSelf(element, clickfunc){
	var items = $(element);
	items.hover(function(){
		$(this).addClass('hover');
	}, function(){
		$(this).removeClass('hover');
	}).click(function(){
		items.removeClass('act');
		var radio = $(this).find(':radio');
		if(radio.length > 0){
			$(this).addClass('act');
			radio.attr('checked', 'checked');
			if(clickfunc){
				clickfunc(this);
			}
		}
	});
}

function nextQuestion(){
	if(index < 10){
		$(questions[index++]).hide();
		$(questions[index]).show();
	}
}