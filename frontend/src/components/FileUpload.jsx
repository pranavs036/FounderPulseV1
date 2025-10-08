import { useState, useRef } from "react";
import { Upload, FileText, CheckCircle2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export const FileUpload = ({ title, description, onUpload, disabled, dataTestId }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (file && onUpload) {
      setUploading(true);
      await onUpload(file);
      setUploading(false);
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  return (
    <Card className="border-2 border-dashed border-slate-200 hover:border-blue-300 transition-colors" data-testid={dataTestId}>
      <CardContent className="pt-6">
        <div className="space-y-4">
          <div className="text-center">
            <div className="mx-auto w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mb-3">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-slate-900 mb-1">{title}</h3>
            <p className="text-xs text-slate-500">{description}</p>
          </div>

          <div className="space-y-2">
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              className="hidden"
              id={`file-input-${dataTestId}`}
              data-testid={`${dataTestId}-input`}
            />
            <Button
              variant="outline"
              size="sm"
              className="w-full"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled || uploading}
              data-testid={`${dataTestId}-select-button`}
            >
              <Upload className="w-4 h-4 mr-2" />
              {file ? "Change File" : "Select File"}
            </Button>

            {file && (
              <div className="text-xs text-slate-600 truncate px-2" data-testid={`${dataTestId}-filename`}>
                {file.name}
              </div>
            )}

            {file && (
              <Button
                size="sm"
                className="w-full bg-blue-600 hover:bg-blue-700"
                onClick={handleUpload}
                disabled={disabled || uploading}
                data-testid={`${dataTestId}-upload-button`}
              >
                {uploading ? (
                  "Uploading..."
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4 mr-2" />
                    Upload
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default FileUpload;