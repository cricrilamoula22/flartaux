$(document).ready(function() {
    // Handle Submit Selected Items
    $('#submit-selected-items').click(function() {
        console.log("Button clicked!");

        // Collect selected left items
        let selectedLeftItems = [];
        $('#select-left-items input[type=checkbox]:checked').each(function() {
            selectedLeftItems.push($(this).data('id'));
        });
        console.log("Selected left items:", selectedLeftItems);

        // Collect selected right items
        let selectedRightItems = [];
        $('#select-right-items input[type=checkbox]:checked').each(function() {
            selectedRightItems.push($(this).data('id'));
        });
        console.log("Selected right items:", selectedRightItems);

        // Get the selected group ID
        let groupId = $('#group-id-select').val();
        console.log("Selected group ID:", groupId);

        // Check if there are selected items and a group
        if ((selectedLeftItems.length > 0 || selectedRightItems.length > 0) && groupId) {
            // Prepare the data to send to the backend
            console.log("Sending data to backend:", {
                group_id: groupId,
                item_ids_left: selectedLeftItems,
                item_ids_right: selectedRightItems,
                side: 'both'
            });

            $.post('/select_items', {
                group_id: groupId,
                item_ids_left: selectedLeftItems, // Send left item IDs
                item_ids_right: selectedRightItems, // Send right item IDs
                side: 'both' // Indicate that we're sending both left and right items
            }, function(response) {
                if (response.success) {
                    alert('Items successfully added to the group!');
                }
            });
        } else {
            alert('Please select at least one item and a group.');
        }
    });
});


$(document).ready(function() {
    // Handle Test Button Click
    $('#test-button').click(function() {
        $.post('/test_add_data', function(response) {
            if (response.success) {
                alert('Test data added to ItemsGroups successfully!');
            }
        });
    });

    // The rest of the script code...
});


$(document).ready(function() {
    // Add Group
    $('#add-group-btn').click(function() {
        $.post('/add_group', function(data) {
            if (data.success) {
                $('#groups-list').append(`
                    <div class="group" data-id="${data.group_id}">
                        <h4>${data.group_name}</h4>
                        <div class="group-items">
                            <div class="left-items-in-group">
                                <h5>Left Items</h5>
                                <div id="left-items-group-${data.group_id}"></div>
                                <button class="select-left-btn" data-group-id="${data.group_id}">Select Left Items</button>
                                <button class="unselect-left-btn" data-group-id="${data.group_id}">Unselect Left Items</button>
                            </div>
                            <div class="right-items-in-group">
                                <h5>Right Items</h5>
                                <div id="right-items-group-${data.group_id}"></div>
                                <button class="select-right-btn" data-group-id="${data.group_id}">Select Right Items</button>
                                <button class="unselect-right-btn" data-group-id="${data.group_id}">Unselect Right Items</button>
                            </div>
                        </div>
                    </div>
                `);
            }
        });
    });
	
	

    // Add Item to Left or Right
    function addItem(side) {
        let name = prompt(`Enter new ${side} item name`);
        if (name) {
            $.post('/add_item', { name: name, side: side }, function(data) {
                if (data.success) {
                    $(`#${side}-items-list`).append(`
                        <li>
                            <input type="checkbox" class="${side}-item-checkbox" data-id="${data.item_id}">
                            ${data.item_name}
                        </li>
                    `);
                }
            });
        }
    }

    $('#add-left-item').click(function() { addItem('left'); });
    $('#add-right-item').click(function() { addItem('right'); });

    // Select Items for Group
    function selectItems(groupId, side) {
    let selectedItems = [];
    $(`#${side}-items-list input[type=checkbox]:checked`).each(function() {
        selectedItems.push($(this).data('id'));
    });

    // Check if selected items are not empty
    if (selectedItems.length > 0) {
        $.ajax({
            url: '/select_items',
            type: 'POST',
            data: {
                group_id: groupId,
                item_ids: selectedItems, // This is what gets passed to the backend
                side: side
            },
            success: function(response) {
                if (response.success) {
                    selectedItems.forEach(itemId => {
                        let itemText = $(`#${side}-items-list li input[data-id=${itemId}]`).closest('li').text();
                        
                        // Move the selected item to the corresponding group section
                        if (side === 'left') {
                            $(`#left-items-group-${groupId}`).append(`<div>${itemText}</div>`);
                        } else {
                            $(`#right-items-group-${groupId}`).append(`<div>${itemText}</div>`);
                        }
                        
                        // Remove item from the original items list
                        $(`#${side}-items-list li input[data-id=${itemId}]`).closest('li').remove();
                    });
                    alert(`${side.charAt(0).toUpperCase() + side.slice(1)} items selected successfully!`);
                }
            }
        });
    }
}


    // Select Left Items
    $('.select-left-btn').click(function() {
        let groupId = $(this).data('group-id');
        selectItems(groupId, 'left');
    });

    // Select Right Items
    $('.select-right-btn').click(function() {
        let groupId = $(this).data('group-id');
        selectItems(groupId, 'right');
    });

    // Unselect Items
    function unselectItems(groupId, side) {
        $.post('/unselect_item', { group_id: groupId, side: side }, function(response) {
            if (response.success) {
                $(`#${side}-items-group-${groupId}`).empty();
                alert(`${side.charAt(0).toUpperCase() + side.slice(1)} items unselected successfully!`);
            }
        });
    }

    // Unselect Left Items
    $('.unselect-left-btn').click(function() {
        let groupId = $(this).data('group-id');
        unselectItems(groupId, 'left');
    });

    // Unselect Right Items
    $('.unselect-right-btn').click(function() {
        let groupId = $(this).data('group-id');
        unselectItems(groupId, 'right');
    });
});
