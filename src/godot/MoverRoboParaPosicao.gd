extends Button
# Called when the node enters the scene tree for the first time.
func _ready():
	self.disabled = true
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")	

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		self.add_color_override("font_color", Color(0, 1, 0))
		yield(get_tree().create_timer(2.0), "timeout")
		self.add_color_override("font_color_disabled", Color(1, 1, 1))
	else:
		self.add_color_override("font_color", Color(1, 0, 0))
		yield(get_tree().create_timer(2.0), "timeout")
		self.add_color_override("font_color_disabled", Color(1, 1, 1))

func _on_MoverRoboParaPosicao_pressed():
	var headers = ["Content-Type: application/json"]
	var j1 = get_parent().get_node("J1/ProgressBar")
	var j2 = get_parent().get_node("J2/ProgressBar")
	var j3 = get_parent().get_node("J3/ProgressBar")
	
	var body = JSON.print({"j1": str(j1.value), "j2": str(j2.value), "j3": str(j3.value)}) 
	$HTTPRequest.request("http://127.0.0.1:3001/move", headers, false, HTTPClient.METHOD_POST, body)
