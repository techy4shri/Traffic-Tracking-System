export interface ProcessedResult {
    vehicleCount: number;
    vehicleNumbers: string[];
    processedImageUrl?: string;
}

export interface FileUploadProps {
    onProcessed: (result: ProcessedResult) => void;
}