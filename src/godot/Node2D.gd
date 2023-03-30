extends Node2D

var preenchido: bool = false

func _ready():
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")
	$HTTPRequest2.connect("request_completed", self, "_on_request2_completed")
	$HTTPRequest2.request("http://127.0.0.1:3001/connect")
	return

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8()).result
		change_main_progress_bar(json[0].j1, json[0].j2, json[0].j3, str(json[0].x), str(json[0].y), str(json[0].z))
		return
		

func _on_request2_completed(result, response_code, headers, body):
	if response_code == 200:
		$GetPosition.disabled = false
		$MoverRoboParaPosicao.disabled = false
	else:
		$GetPosition.disabled = true
		$MoverRoboParaPosicao.disabled = true
	
	
func _on_LastPosition_pressed():
	$HTTPRequest.request("http://127.0.0.1:3001/all")
	return

func _on_Clear_pressed():
	change_main_progress_bar(-139, -3, -8, "", "", "")
	preenchido = false
	
func change_main_progress_bar(j1, j2, j3, x, y, z):
	if preenchido == true:
		$UltimaBusca/Juntas/J1/ProgressBar.value = $J1/ProgressBar.value
		$UltimaBusca/Juntas/J2/ProgressBar.value = $J2/ProgressBar.value
		$UltimaBusca/Juntas/J3/ProgressBar.value = $J3/ProgressBar.value
		var string = "x = %s, y = %s, z = %s"
		$UltimaBusca/Cords.text = string % [$Posicionamento/ResulX.text, $Posicionamento/ResulY.text, $Posicionamento/ResulZ.text]
	
	# Junta 1 vai de 90 a -90
	$J1/ProgressBar.value = j1
	# Junta 2 vai de -4 a 80
	$J2/ProgressBar.value = j2
	# Junta 3 vai de -4 a 80
	$J3/ProgressBar.value = j3
	
	$Posicionamento/ResulX.text = x
	$Posicionamento/ResulY.text = y
	$Posicionamento/ResulZ.text = z
	preenchido = true