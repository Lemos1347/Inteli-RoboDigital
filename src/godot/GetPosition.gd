extends Button

# Called when the node enters the scene tree for the first time.
func _ready():
	self.disabled = true
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		self.add_color_override("font_color", Color(0, 1, 0))
		self.add_color_override("font_color_focus", Color(0, 1, 0))
		yield(get_tree().create_timer(2.0), "timeout")
		self.add_color_override("font_color", Color(1, 1, 1))
		self.add_color_override("font_color_focus", Color(1, 1, 1))
	else:
		self.add_color_override("font_color", Color(1, 0, 0))
		self.add_color_override("font_color_focus", Color(1, 0, 0))
		yield(get_tree().create_timer(2.0), "timeout")
		self.add_color_override("font_color", Color(1, 1, 1))
		self.add_color_override("font_color_focus", Color(1, 1, 1))

func _on_GetPosition_pressed():
	$HTTPRequest.request("http://127.0.0.1:3001/pose")
