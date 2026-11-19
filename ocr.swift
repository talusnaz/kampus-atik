import Foundation
import Vision
import AppKit
if CommandLine.arguments.count > 1,
   let img = NSImage(contentsOfFile: CommandLine.arguments[1]),
   let tiff = img.tiffRepresentation,
   let bmp = NSBitmapImageRep(data: tiff),
   let cg = bmp.cgImage {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    req.results?.compactMap { $0.topCandidates(1).first?.string }.forEach { print($0) }
}
