using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TEST_TRINITY : MonoBehaviour {
	public float Acceleration;
	public ParticleSystem ThrusterVFX;
	public float ThrustTime;

	private bool _isThrusterActive;
	private bool _thrusterActivated;
	private Rigidbody _rb;

	private float t_thruster;

	private void Awake() {
		_rb = GetComponent<Rigidbody>();
		ThrusterVFX.Stop();
	}

	private void Start() {
		ThrusterVFX.Stop();
	}

	void Update() {
		// Check for input
		if (Input.GetKeyDown(KeyCode.Space) && !_thrusterActivated) {
			_isThrusterActive = true;
			_thrusterActivated = true;
			ThrusterVFX.Play();
		}

	}

	private void FixedUpdate() {
		// Thruster
		if (_isThrusterActive) {
			if (t_thruster < ThrustTime) {
				_rb.AddForce(Vector3.up * Acceleration, ForceMode.Acceleration);
				t_thruster += Time.fixedDeltaTime;
			}
			else {
				_isThrusterActive = false;
				ThrusterVFX.Stop();
			}
		}
	}
}