using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TrinityUI : MonoBehaviour {
	public GameObject TrinityObject;
	public TextMeshProUGUI AltitudeText;

	private void Update() {
		AltitudeText.text = TrinityObject.transform.position.y.ToString("0.00") + " ft";
	}
}