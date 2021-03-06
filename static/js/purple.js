// cache DOM ojects
var $grid = $('#player-grid');
var raw_data = { reb : 0, ast : 0, stl : 0, blk : 0, fga : 0, fgm : 0, tga : 0, tgm : 0, fta : 0, ftm : 0, to : 0 }

// define calculations
function update_overall_points(row) {
    var field_goals = parseInt(row.cells[1].children[0].innerHTML);
    var pointers    = parseInt(row.cells[2].children[0].innerHTML);
    var free_throws = parseInt(row.cells[3].children[0].innerHTML);
    var overall_points = (field_goals * 2) + (pointers * 3) + (free_throws * 1);
    row.cells[9].children[0].innerHTML = overall_points;
}
function calculate_efficiency(row) {
    // NBA EFFICIENCY
    // PTS + REB + AST + STL + BLK - (FGA-FGM) - (FTA-FTM) - TO
    row = $(row);
    var data = row.data('stats');
    // follow DRY
    function _clean_value(className) {
        return data[className] = parseInt(row.find('.'+className).html());
    }
    var points   = _clean_value('points');
    var rebounds = _clean_value('reb');
    var assists  = _clean_value('ast');
    var steals   = _clean_value('stl');
    var blocks   = _clean_value('blk');
    var fga      = _clean_value('fga');
    var fgm      = _clean_value('fgm');
    var tga      = _clean_value('tga');
    var tgm      = _clean_value('tgm');
    var fta      = _clean_value('fta');
    var ftm      = _clean_value('ftm');
    var turnovers= _clean_value('to');
    var efficiency = points + rebounds + assists + steals + blocks - ((fga+tga)-(fgm+tgm)) - (fta-ftm) - turnovers;
    row.find('.eff').html(efficiency);
    row.data('stats',data);
}

/// TODO: Calculate PER

// define event handlers
function stat_adjustment(e) {
    // prepare
    var $t       = $(this);
    var modifier = $grid.hasClass('append') ? 1 : -1;
    var original = parseInt(this.innerHTML);
    // skip if attempts go below points
    var prev = $t.prev('a.attempt').get();
    var pval = !!prev.length ? parseInt(prev[0].innerHTML) : false;
    if ( (!!pval && pval == original && modifier < 0) || (original + (1 * modifier)) < 0) { return }
    // make changes to value
    var value    = original + (1 * modifier);
    this.innerHTML = value;
    
    // apply to attempts if true
    if ($t.hasClass("attempt")) {
        var sibling = $t.next('a');
        value = parseInt(sibling[0].innerHTML) + (1 * modifier);
        sibling[0].innerHTML = value;
    }
    // now update the points
    update_overall_points(this.parentNode.parentNode);
    // finally calculate nba efficiency
    calculate_efficiency(this.parentNode.parentNode);
}

function create_row(name,db_key) {
    var add_row = $grid.find('#add-player');
    var new_row = add_row.clone().attr('id',db_key);
    new_row.data('stats',$.extend({},raw_data));
    new_row.find('th').html(name);
    new_row.insertBefore(add_row);
}

function add_player_to_roster(e) {
    var t = this;
    $.getJSON('/purple/add_player', { 'name' : this.value }, function(d) {
        if (d.player) {
            create_row(t.value, d.player);
            t.value = "";
        }
    });
}

function on_enter(fn) {
    return function(e) {
        return e.which == 13 ? fn.call(this,e) : true;
    }
}

// bind events
jQuery(function($){
    // load roster
    if (window.players) {
        var current;
        for (var i=0;i<window.players.length;i++) {
            create_row.apply(undefined,window.players[i]);
        }
    }
    
    // bind events
    document.onselectstart = function(e){return false;}
    document.onmousedown   = function(e){if (e.target.nodeName === "INPUT") { return true; } return false;}
    $('tbody',$grid).on('click','a',stat_adjustment);
    $grid.find('#add-player input').bind('keypress',on_enter(add_player_to_roster));
    
    $grid.find('#change').bind('click',function(e){
        var cn = $grid[0].className;
        $grid.removeClass(cn).addClass(cn == "append" ? "subtract" : "append");
    });
    
    // check game at end of session
    $(window).unload(function(e){
        $.ajax({
            async : false,
            url   : '/purple/cleanup',
            data  : {},
            method: 'POST',
        })
    });
});