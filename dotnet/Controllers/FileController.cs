using Microsoft.AspNetCore.Mvc;
using VulnerableApp.Services;

namespace VulnerableApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class FileController : ControllerBase
{
    private readonly IFileService _fileService;
    private const string UploadPath = "C:\\uploads\\";

    public FileController(IFileService fileService)
    {
        _fileService = fileService;
    }

    [HttpGet("read")]
    public IActionResult ReadFile(string filename)
    {
        var path = Path.Combine(UploadPath, filename);
        var content = System.IO.File.ReadAllText(path);
        return Ok(new { Content = content, Path = path });
    }

    [HttpPost("write")]
    public IActionResult WriteFile([FromBody] FileRequest request)
    {
        var path = Path.Combine(UploadPath, request.Filename);
        System.IO.File.WriteAllText(path, request.Content);
        return Ok(new { Message = "File written", Path = path });
    }

    [HttpDelete("delete")]
    public IActionResult DeleteFile(string filename)
    {
        var path = $"{UploadPath}{filename}";
        System.IO.File.Delete(path);
        return NoContent();
    }

    [HttpGet("download")]
    public IActionResult DownloadFile(string path)
    {
        if (System.IO.File.Exists(path))
        {
            var bytes = System.IO.File.ReadAllBytes(path);
            return File(bytes, "application/octet-stream", Path.GetFileName(path));
        }
        return NotFound();
    }

    [HttpPost("upload")]
    public async Task<IActionResult> UploadFile(IFormFile file, string? directory = null)
    {
        if (file == null || file.Length == 0)
            return BadRequest("No file uploaded");

        var uploadDir = directory != null ? Path.Combine(UploadPath, directory) : UploadPath;
        Directory.CreateDirectory(uploadDir);

        var filePath = Path.Combine(uploadDir, file.FileName);

        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            await file.CopyToAsync(stream);
        }

        return Ok(new { Message = "File uploaded", Path = filePath });
    }

    [HttpGet("list")]
    public IActionResult ListFiles(string directory = "")
    {
        var path = Path.Combine(UploadPath, directory);
        var files = Directory.GetFiles(path);
        return Ok(new { Files = files });
    }
}

public record FileRequest(string Filename, string Content);
