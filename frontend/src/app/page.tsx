"use client";

import { useState } from "react";
import NextImage from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { 
  Upload, 
  Type, 
  Smile, 
  Play, 
  Download, 
  CheckCircle2, 
  AlertCircle,
  Image as ImageIcon,
  Sparkles
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function AvatarPage() {
  const [text, setText] = useState("");
  const [emotion, setEmotion] = useState("neutral");
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState<string[]>([]);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const emotions = [
    { label: "Neutral", value: "neutral" },
    { label: "Happy", value: "happy" },
    { label: "Sad", value: "sad" },
    { label: "Angry", value: "angry" },
    { label: "Excited", value: "excited" },
    { label: "Surprised", value: "surprised" },
    { label: "Confused", value: "confused" },
  ];

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const generateAvatar = async () => {
    if (!image || !text) return;
    setLoading(true);
    setError(null);
    setVideoUrl(null);
    setProgress(["Initializing AI components..."]);

    const formData = new FormData();
    formData.append("image", image);
    formData.append("text", text);
    formData.append("emotion", emotion);

    try {
      const steps = [
        "Enhancing Image (GFPGAN/ESRGAN)...",
        "3D Face Reconstruction (DECA)...",
        "Lip-Sync & Rendering (D-ID)..."
      ];
      
      let currentStep = 0;
      const interval = setInterval(() => {
        if (currentStep < steps.length) {
          setProgress(prev => [...prev, steps[currentStep]]);
          currentStep++;
        } else {
          clearInterval(interval);
        }
      }, 2500);

      const response = await fetch("http://localhost:8000/generate-avatar", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      clearInterval(interval);

      if (!response.ok) throw new Error(data.detail || "Generation failed");

      setVideoUrl(data.video_url);
      setProgress(prev => [...prev, "Pipeline complete!"]);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Generation failed";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Avatar Module</h1>
        <p className="text-slate-500">Transform static images into professional 3D talking avatars.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Configuration */}
        <div className="lg:col-span-5 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <ImageIcon className="h-5 w-5 text-blue-600" />
                Identity Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div 
                className={cn(
                  "group relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed transition-all",
                  preview ? "border-blue-400 bg-blue-50/30 p-2" : "border-slate-200 py-12 hover:border-slate-300 hover:bg-slate-50"
                )}
              >
                {preview ? (
                  <div className="relative aspect-square w-full max-w-[240px] rounded-lg overflow-hidden shadow-lg group-hover:opacity-90 transition-opacity">
                    <NextImage src={preview} alt="Identity Preview" className="h-full w-full object-cover" fill unoptimized />
                    <label className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                      <Button variant="secondary" size="sm">Change Photo</Button>
                      <input type="file" className="hidden" accept="image/*" onChange={handleImageChange} />
                    </label>
                  </div>
                ) : (
                  <label className="flex flex-col items-center justify-center cursor-pointer text-center px-4">
                    <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center mb-4 group-hover:bg-blue-100 transition-colors">
                      <Upload className="h-6 w-6 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <span className="text-sm font-semibold text-slate-900">Upload Portrait</span>
                    <span className="text-xs text-slate-500 mt-1">High-res JPG/PNG supported</span>
                    <input type="file" className="hidden" accept="image/*" onChange={handleImageChange} />
                  </label>
                )}
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <Type className="h-4 w-4" />
                  Speech Script
                </div>
                <textarea
                  className="w-full min-h-[120px] rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm transition-all focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-500/10 outline-none"
                  placeholder="Enter the text your avatar will speak..."
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <Smile className="h-4 w-4" />
                  Emotional Expression
                </div>
                <div className="grid grid-cols-4 gap-2">
                  {emotions.map((e) => (
                    <button
                      key={e.value}
                      onClick={() => setEmotion(e.value)}
                      className={cn(
                        "rounded-lg border px-3 py-2 text-xs font-medium transition-all",
                        emotion === e.value
                          ? "border-blue-600 bg-blue-600 text-white shadow-md shadow-blue-200"
                          : "border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50"
                      )}
                    >
                      {e.label}
                    </button>
                  ))}
                </div>
              </div>

              <Button 
                className="w-full shadow-lg shadow-blue-200" 
                size="lg"
                disabled={!image || !text}
                isLoading={loading}
                onClick={generateAvatar}
              >
                Generate 3D Avatar
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Right: Output */}
        <div className="lg:col-span-7 space-y-6">
          <Card className="min-h-[600px] flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between border-b border-slate-100">
              <CardTitle className="text-lg flex items-center gap-2">
                <Play className="h-5 w-5 text-blue-600" />
                Production Preview
              </CardTitle>
              {videoUrl && (
                <Button variant="outline" size="sm" className="gap-2">
                  <Download className="h-4 w-4" />
                  Export MP4
                </Button>
              )}
            </CardHeader>
            <CardContent className="flex-grow flex flex-col items-center justify-center p-8">
              {videoUrl ? (
                <div className="w-full rounded-2xl overflow-hidden bg-black shadow-2xl ring-8 ring-slate-50 aspect-video">
                  <video src={videoUrl} controls autoPlay className="h-full w-full object-contain" />
                </div>
              ) : loading ? (
                <div className="w-full max-w-md space-y-8 animate-in zoom-in-95 duration-300">
                  <div className="flex flex-col items-center text-center">
                    <div className="relative h-20 w-20 mb-6">
                      <div className="absolute inset-0 border-4 border-blue-100 rounded-full" />
                      <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">Orchestrating AI Pipeline</h3>
                    <p className="text-slate-500 text-sm mt-1">Please wait while we render your avatar.</p>
                  </div>
                  <div className="space-y-3">
                    {progress.map((p, i) => (
                      <div key={i} className="flex items-center gap-3 rounded-lg bg-slate-50 p-3 text-sm font-medium text-slate-700 animate-in slide-in-from-left-2 duration-500">
                        <div className="flex h-5 w-5 items-center justify-center rounded-full bg-green-100">
                          <CheckCircle2 className="h-3.5 w-3.5 text-green-600" />
                        </div>
                        {p}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center text-center p-12 bg-slate-50/50 rounded-3xl border border-dashed border-slate-200">
                  <div className="h-16 w-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-6">
                    <Sparkles className="h-8 w-8 text-slate-300" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">Render Ready</h3>
                  <p className="text-slate-500 text-sm max-w-[280px]">Complete the configuration to start the production pipeline.</p>
                </div>
              )}

              {error && (
                <div className="mt-8 w-full max-w-md rounded-xl bg-red-50 border border-red-100 p-4 flex items-start gap-3 animate-in shake-in duration-300">
                  <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                  <div className="flex-1 text-sm font-medium text-red-700">{error}</div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
