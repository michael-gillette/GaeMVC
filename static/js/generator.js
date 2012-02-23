// cache dom
var $target = $('#target');

function modify_border_radius(e) {
    // prepare
    var current_value = !!this.value ? parseInt(this.value) : this.value = 0;
    
    // value shall not be negative
    if (current_value < 0) { current_value=this.value=0; }
    
    // adjust
    $target.css('-webkit-border-'+this.id+'-radius',current_value+'px');
}

function capture_adjustment(e) {
    // modify border radius
    if (e.which == 38)      this.value = parseInt(this.value) + 1
    else if (e.which == 40) this.value = parseInt(this.value) - 1
    else if (e.which > 31 && (e.which < 48 || e.which > 57)) return false;
    
    // implement change on preview
    modify_border_radius.call(this,e);
}

jQuery(function($){
    $('.radii')
        .bind('blur',modify_border_radius)
        .bind('keypress keydown',capture_adjustment);
});