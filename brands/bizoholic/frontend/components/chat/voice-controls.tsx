"use client"

import React, { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Slider } from '@/components/ui/slider'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import {
  Mic, MicOff, Volume2, VolumeX, Settings, Play, Pause,
  AlertCircle, CheckCircle, Loader2, Headphones
} from 'lucide-react'
import { VoiceInterfaceManager, VoiceSettings, VoiceState, VoiceRecognitionResult } from '@/lib/voice-interface'

interface VoiceControlsProps {
  onVoiceInput?: (text: string, confidence: number) => void
  onSpeakResponse?: (speakFn: (text: string) => Promise<void>) => void
  autoSpeakResponses?: boolean
  className?: string
}

export function VoiceControls({
  onVoiceInput,
  onSpeakResponse,
  autoSpeakResponses = false,
  className = ""
}: VoiceControlsProps) {
  const voiceManager = useRef<VoiceInterfaceManager | null>(null)
  const [voiceState, setVoiceState] = useState<VoiceState>({
    isListening: false,
    isRecognizing: false,
    isSpeaking: false,
    hasPermission: false,
    error: null
  })
  const [settings, setSettings] = useState<VoiceSettings>({
    enabled: false,
    speechToText: {
      enabled: true,
      language: 'en-US',
      continuous: false,
      interimResults: true
    },
    textToSpeech: {
      enabled: true,
      voice: '',
      rate: 1.0,
      pitch: 1.0,
      volume: 0.8
    },
    autoPlayResponses: autoSpeakResponses,
    voiceActivation: false,
    noiseReduction: true
  })
  const [showSettings, setShowSettings] = useState(false)
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([])
  const [currentTranscript, setCurrentTranscript] = useState('')
  const [confidence, setConfidence] = useState(0)

  // Initialize voice manager
  useEffect(() => {
    voiceManager.current = new VoiceInterfaceManager(settings)

    voiceManager.current.setCallbacks({
      onStateChange: (state) => {
        setVoiceState(state)
      },
      onResult: (result) => {
        setCurrentTranscript(result.transcript)
        setConfidence(result.confidence)

        if (result.isFinal && onVoiceInput) {
          onVoiceInput(result.transcript, result.confidence)
          setCurrentTranscript('')
          setConfidence(0)
        }
      },
      onError: (error) => {
        console.error('Voice interface error:', error)
      }
    })

    // Load available voices
    const updateVoices = () => {
      if (voiceManager.current) {
        const voices = voiceManager.current.getAvailableVoices()
        setAvailableVoices(voices)

        // Set default voice if none selected
        if (!settings.textToSpeech.voice && voices.length > 0) {
          const defaultVoice = voices.find(voice => voice.default) || voices[0]
          updateVoiceSettings({
            textToSpeech: {
              ...settings.textToSpeech,
              voice: defaultVoice.name
            }
          })
        }
      }
    }

    updateVoices()

    // Some browsers load voices asynchronously
    if ('speechSynthesis' in window) {
      window.speechSynthesis.onvoiceschanged = updateVoices
    }

    return () => {
      if (voiceManager.current) {
        voiceManager.current.destroy()
      }
    }
  }, [])

  // Handle auto-speak responses
  useEffect(() => {
    if (settings.autoPlayResponses !== autoSpeakResponses) {
      updateVoiceSettings({
        autoPlayResponses: autoSpeakResponses
      })
    }
  }, [autoSpeakResponses])

  const updateVoiceSettings = (newSettings: Partial<VoiceSettings>) => {
    const updatedSettings = { ...settings, ...newSettings }
    setSettings(updatedSettings)

    if (voiceManager.current) {
      voiceManager.current.updateSettings(updatedSettings)
    }
  }

  const toggleVoiceInterface = async () => {
    if (!voiceManager.current) return

    const newEnabled = !settings.enabled
    updateVoiceSettings({ enabled: newEnabled })

    if (newEnabled && !voiceState.hasPermission) {
      await voiceManager.current.requestPermission()
    }
  }

  const toggleListening = async () => {
    if (!voiceManager.current || !settings.enabled) return

    if (voiceState.isListening) {
      voiceManager.current.stopListening()
    } else {
      await voiceManager.current.startListening()
    }
  }

  const speakText = async (text: string) => {
    if (voiceManager.current && settings.enabled) {
      await voiceManager.current.speakText(text)
    }
  }

  const stopSpeaking = () => {
    if (voiceManager.current) {
      voiceManager.current.stopSpeaking()
    }
  }

  // Expose speak function for parent component
  useEffect(() => {
    if (onSpeakResponse) {
      onSpeakResponse(speakText)
    }
  }, [onSpeakResponse])

  const support = voiceManager.current?.isSupported() || {
    speechToText: false,
    textToSpeech: false
  }

  // Don't render if no voice support
  if (!support.speechToText && !support.textToSpeech) {
    return null
  }

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Voice Enable Toggle */}
      <Button
        variant={settings.enabled ? "default" : "outline"}
        size="sm"
        onClick={toggleVoiceInterface}
        className="flex items-center space-x-1"
      >
        <Headphones className="w-4 h-4" />
        <span className="hidden sm:inline">
          {settings.enabled ? 'Voice On' : 'Voice Off'}
        </span>
      </Button>

      {settings.enabled && (
        <>
          {/* Speech-to-Text Controls */}
          {support.speechToText && (
            <div className="flex items-center space-x-1">
              <Button
                variant={voiceState.isListening ? "destructive" : "outline"}
                size="sm"
                onClick={toggleListening}
                disabled={!voiceState.hasPermission}
                className="relative"
              >
                {voiceState.isListening ? (
                  <MicOff className="w-4 h-4" />
                ) : (
                  <Mic className="w-4 h-4" />
                )}

                {voiceState.isRecognizing && (
                  <div className="absolute -top-1 -right-1 w-3 h-3">
                    <Loader2 className="w-3 h-3 animate-spin text-blue-500" />
                  </div>
                )}
              </Button>

              {currentTranscript && (
                <Badge variant="secondary" className="max-w-32 truncate">
                  {Math.round(confidence * 100)}% - {currentTranscript}
                </Badge>
              )}
            </div>
          )}

          {/* Text-to-Speech Controls */}
          {support.textToSpeech && (
            <Button
              variant={voiceState.isSpeaking ? "destructive" : "outline"}
              size="sm"
              onClick={voiceState.isSpeaking ? stopSpeaking : undefined}
              className="relative"
            >
              {voiceState.isSpeaking ? (
                <VolumeX className="w-4 h-4" />
              ) : (
                <Volume2 className="w-4 h-4" />
              )}

              {voiceState.isSpeaking && (
                <div className="absolute -top-1 -right-1 w-3 h-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                </div>
              )}
            </Button>
          )}

          {/* Voice Settings */}
          <Dialog open={showSettings} onOpenChange={setShowSettings}>
            <DialogTrigger asChild>
              <Button variant="ghost" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
            </DialogTrigger>

            <DialogContent className="max-w-lg">
              <DialogHeader>
                <DialogTitle className="flex items-center space-x-2">
                  <Headphones className="w-5 h-5" />
                  <span>Voice Settings</span>
                </DialogTitle>
              </DialogHeader>

              <div className="space-y-6">
                {/* Feature Support Status */}
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">Feature Support</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Speech Recognition:</span>
                      <div className="flex items-center space-x-1">
                        {support.speechToText ? (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-red-500" />
                        )}
                        <span className="text-sm">
                          {support.speechToText ? 'Supported' : 'Not Supported'}
                        </span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Text-to-Speech:</span>
                      <div className="flex items-center space-x-1">
                        {support.textToSpeech ? (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-red-500" />
                        )}
                        <span className="text-sm">
                          {support.textToSpeech ? 'Supported' : 'Not Supported'}
                        </span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Microphone Permission:</span>
                      <div className="flex items-center space-x-1">
                        {voiceState.hasPermission ? (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-orange-500" />
                        )}
                        <span className="text-sm">
                          {voiceState.hasPermission ? 'Granted' : 'Required'}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Speech-to-Text Settings */}
                {support.speechToText && (
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">Speech Recognition</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="stt-enabled">Enable Speech Input</Label>
                        <Switch
                          id="stt-enabled"
                          checked={settings.speechToText.enabled}
                          onCheckedChange={(enabled) =>
                            updateVoiceSettings({
                              speechToText: { ...settings.speechToText, enabled }
                            })
                          }
                        />
                      </div>

                      <div className="space-y-2">
                        <Label>Language</Label>
                        <Select
                          value={settings.speechToText.language}
                          onValueChange={(language) =>
                            updateVoiceSettings({
                              speechToText: { ...settings.speechToText, language }
                            })
                          }
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="en-US">English (US)</SelectItem>
                            <SelectItem value="en-GB">English (UK)</SelectItem>
                            <SelectItem value="es-ES">Spanish</SelectItem>
                            <SelectItem value="fr-FR">French</SelectItem>
                            <SelectItem value="de-DE">German</SelectItem>
                            <SelectItem value="it-IT">Italian</SelectItem>
                            <SelectItem value="ja-JP">Japanese</SelectItem>
                            <SelectItem value="ko-KR">Korean</SelectItem>
                            <SelectItem value="zh-CN">Chinese (Simplified)</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="flex items-center justify-between">
                        <Label htmlFor="continuous">Continuous Listening</Label>
                        <Switch
                          id="continuous"
                          checked={settings.speechToText.continuous}
                          onCheckedChange={(continuous) =>
                            updateVoiceSettings({
                              speechToText: { ...settings.speechToText, continuous }
                            })
                          }
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label htmlFor="interim">Show Interim Results</Label>
                        <Switch
                          id="interim"
                          checked={settings.speechToText.interimResults}
                          onCheckedChange={(interimResults) =>
                            updateVoiceSettings({
                              speechToText: { ...settings.speechToText, interimResults }
                            })
                          }
                        />
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Text-to-Speech Settings */}
                {support.textToSpeech && (
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">Text-to-Speech</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="tts-enabled">Enable Speech Output</Label>
                        <Switch
                          id="tts-enabled"
                          checked={settings.textToSpeech.enabled}
                          onCheckedChange={(enabled) =>
                            updateVoiceSettings({
                              textToSpeech: { ...settings.textToSpeech, enabled }
                            })
                          }
                        />
                      </div>

                      <div className="space-y-2">
                        <Label>Voice</Label>
                        <Select
                          value={settings.textToSpeech.voice}
                          onValueChange={(voice) =>
                            updateVoiceSettings({
                              textToSpeech: { ...settings.textToSpeech, voice }
                            })
                          }
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select voice" />
                          </SelectTrigger>
                          <SelectContent className="max-h-48">
                            {availableVoices.map((voice) => (
                              <SelectItem key={voice.name} value={voice.name}>
                                <div className="flex items-center justify-between w-full">
                                  <span>{voice.name}</span>
                                  <div className="flex items-center space-x-1">
                                    <Badge variant="outline" className="text-xs">
                                      {voice.lang}
                                    </Badge>
                                    {voice.default && (
                                      <Badge variant="secondary" className="text-xs">
                                        Default
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label>Speech Rate: {settings.textToSpeech.rate.toFixed(1)}</Label>
                        <Slider
                          value={[settings.textToSpeech.rate]}
                          onValueChange={([rate]) =>
                            updateVoiceSettings({
                              textToSpeech: { ...settings.textToSpeech, rate }
                            })
                          }
                          min={0.5}
                          max={2.0}
                          step={0.1}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label>Pitch: {settings.textToSpeech.pitch.toFixed(1)}</Label>
                        <Slider
                          value={[settings.textToSpeech.pitch]}
                          onValueChange={([pitch]) =>
                            updateVoiceSettings({
                              textToSpeech: { ...settings.textToSpeech, pitch }
                            })
                          }
                          min={0.5}
                          max={2.0}
                          step={0.1}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label>Volume: {Math.round(settings.textToSpeech.volume * 100)}%</Label>
                        <Slider
                          value={[settings.textToSpeech.volume]}
                          onValueChange={([volume]) =>
                            updateVoiceSettings({
                              textToSpeech: { ...settings.textToSpeech, volume }
                            })
                          }
                          min={0.1}
                          max={1.0}
                          step={0.1}
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <Label htmlFor="auto-play">Auto-play AI Responses</Label>
                        <Switch
                          id="auto-play"
                          checked={settings.autoPlayResponses}
                          onCheckedChange={(autoPlayResponses) =>
                            updateVoiceSettings({ autoPlayResponses })
                          }
                        />
                      </div>

                      {/* Voice Test */}
                      <div className="pt-2">
                        <Button
                          onClick={() => speakText("This is a test of the text-to-speech system.")}
                          disabled={voiceState.isSpeaking || !settings.textToSpeech.enabled}
                          className="w-full"
                        >
                          <Play className="w-4 h-4 mr-2" />
                          Test Voice
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Error Display */}
                {voiceState.error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{voiceState.error}</AlertDescription>
                  </Alert>
                )}

                <Button
                  onClick={() => setShowSettings(false)}
                  className="w-full"
                >
                  Close Settings
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </>
      )}

      {/* Status Indicators */}
      {settings.enabled && (
        <div className="flex items-center space-x-1">
          {voiceState.isListening && (
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
              <span className="text-xs text-muted-foreground hidden sm:inline">Listening</span>
            </div>
          )}
          {voiceState.isSpeaking && (
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs text-muted-foreground hidden sm:inline">Speaking</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}