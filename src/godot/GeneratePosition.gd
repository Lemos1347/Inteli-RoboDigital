extends Button

func _ready():
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8()).result
		var j1 = json.j1
		get_parent().change_main_progress_bar(json.j1, json.j2, json.j3, str(json.x), str(json.y), str(json.z))


func _on_GeneratePosition_pressed():
	var selected_id = $Positions.get_selected_id()
	var selected_value = $Positions.get_item_text(selected_id)
	var url = "http://127.0.0.1:3001/id/%s"
	$HTTPRequest.request(url % selected_value)
	return
