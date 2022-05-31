$('.drag').draggable({ 
  appendTo: 'body',
  helper: 'clone'
});

$('#dropzone').droppable({
  activeClass: 'active_drag',
  hoverClass: 'hover',
  accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
  drop: function (e, ui) {
    var $el = $('<div class="drop-item">' + ui.draggable.text() + '</div>');
    $el.append($('<button type="button" class="btn btn-primary remove"><span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" ></span></button>').click(function () { $(this).parent().detach(); }));
    $(this).append($el);
  }
}).sortable({
  items: '.drop-item',
  sort: function() {
    // gets added unintentionally by droppable interacting with sortable
    // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
    $( this ).removeClass( "active_drag" );
  }
});