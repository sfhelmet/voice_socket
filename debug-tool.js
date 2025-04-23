// debug-tool.js (JavaScript to add to your HTML or use in browser console)

// This function checks a peer connection and logs all its important states
function debugRTCPeerConnection(pc) {
    if (!pc) {
        console.log('No peer connection to debug');
        return;
    }
    
    console.log('--- WebRTC Connection Debug ---');
    console.log('Signaling State:', pc.signalingState);
    console.log('Connection State:', pc.connectionState);
    console.log('ICE Connection State:', pc.iceConnectionState);
    console.log('ICE Gathering State:', pc.iceGatheringState);
    
    // Get and log all transceivers
    const transceivers = pc.getTransceivers();
    console.log('Transceivers:', transceivers.length);
    transceivers.forEach((transceiver, i) => {
        console.log(`Transceiver ${i}:`, {
            currentDirection: transceiver.currentDirection,
            direction: transceiver.direction,
            stopped: transceiver.stopped
        });
    });
    
    // Get all stats to analyze
    pc.getStats().then(stats => {
        let audioInputLevel = null;
        let audioOutputLevel = null;
        let packetsReceived = 0;
        let packetsSent = 0;
        let packetsLost = 0;
        
        stats.forEach(report => {
            if (report.type === 'inbound-rtp' && report.kind === 'audio') {
                packetsReceived = report.packetsReceived;
                packetsLost = report.packetsLost;
                if (report.audioLevel) {
                    audioOutputLevel = report.audioLevel;
                }
            }
            
            if (report.type === 'outbound-rtp' && report.kind === 'audio') {
                packetsSent = report.packetsSent;
                if (report.audioLevel) {
                    audioInputLevel = report.audioLevel;
                }
            }
        });
        
        console.log('Audio Stats:', {
            inputLevel: audioInputLevel,
            outputLevel: audioOutputLevel,
            packetsSent,
            packetsReceived,
            packetsLost
        });
    });
}

// Call this function to test for audio issues
function testAudio() {
    console.log('Testing audio devices...');
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log('✅ Microphone access successful');
            
            // Create an audio context
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Create an audio analyser
            const analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            
            // Create a source from the stream
            const source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);
            
            // Get frequency data
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            // Check if audio is being detected
            let silenceCounter = 0;
            const checkAudio = () => {
                analyser.getByteFrequencyData(dataArray);
                
                // Calculate average volume
                const average = dataArray.reduce((a, b) => a + b) / bufferLength;
                console.log('Audio level:', average);
                
                if (average < 10) {
                    silenceCounter++;
                } else {
                    console.log('✅ Audio input detected');
                    silenceCounter = 0;
                }
                
                if (silenceCounter > 5) {
                    console.log('⚠️ Warning: No audio input detected. Please check your microphone.');
                }
                
                // Check a few times
                if (silenceCounter < 10) {
                    setTimeout(checkAudio, 500);
                } else {
                    // Clean up
                    stream.getTracks().forEach(track => track.stop());
                }
            };
            
            checkAudio();
        })
        .catch(error => {
            console.error('❌ Microphone access failed:', error);
        });
}

// Call this to check browser WebRTC compatibility
function checkWebRTCSupport() {
    console.log('Checking WebRTC support...');
    
    const report = {
        RTCPeerConnection: !!window.RTCPeerConnection,
        getUserMedia: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
        audioContext: !!(window.AudioContext || window.webkitAudioContext),
        browser: getBrowser()
    };
    
    console.log('WebRTC Support:', report);
    return report.RTCPeerConnection && report.getUserMedia;
}

// Helper to identify browser
function getBrowser() {
    const ua = navigator.userAgent;
    let browser = "Unknown";
    
    if (ua.indexOf("Chrome") > -1) browser = "Chrome";
    else if (ua.indexOf("Safari") > -1) browser = "Safari";
    else if (ua.indexOf("Firefox") > -1) browser = "Firefox";
    else if (ua.indexOf("Edge") > -1) browser = "Edge";
    else if (ua.indexOf("MSIE") > -1 || ua.indexOf("Trident") > -1) browser = "IE";
    
    return browser;
}

// Use these in browser console:
// checkWebRTCSupport() - Check if browser supports WebRTC
// testAudio() - Test microphone access and input levels
// debugRTCPeerConnection(peerConnection) - Debug existing connection