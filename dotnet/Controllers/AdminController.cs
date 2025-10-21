using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Xml;
using Newtonsoft.Json;

namespace VulnerableApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AdminController : ControllerBase
{
    private const string AdminPassword = "admin123";
    private const string ApiSecret = "secret-api-key-xyz";

    [HttpPost("execute")]
    public IActionResult ExecuteCommand([FromBody] CommandRequest request)
    {
        var processInfo = new ProcessStartInfo("cmd.exe", $"/c {request.Command}")
        {
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = Process.Start(processInfo);
        using var reader = process!.StandardOutput;
        var output = reader.ReadToEnd();

        return Ok(new { Output = output, Command = request.Command });
    }

    [HttpPost("ping")]
    public IActionResult Ping([FromBody] PingRequest request)
    {
        var processInfo = new ProcessStartInfo("ping", $"-n 4 {request.Host}")
        {
            RedirectStandardOutput = true,
            UseShellExecute = false
        };

        using var process = Process.Start(processInfo);
        using var reader = process!.StandardOutput;
        var output = reader.ReadToEnd();

        return Ok(output);
    }

    [HttpPost("deserialize")]
    public IActionResult Deserialize([FromBody] DeserializeRequest request)
    {
        try
        {
            var settings = new JsonSerializerSettings
            {
                TypeNameHandling = TypeNameHandling.All
            };

            var obj = JsonConvert.DeserializeObject(request.Data, settings);
            return Ok(new { Result = obj?.ToString() });
        }
        catch (Exception ex)
        {
            return BadRequest(new
            {
                Error = ex.Message,
                StackTrace = ex.StackTrace,
                InnerException = ex.InnerException?.Message
            });
        }
    }

    [HttpPost("xml")]
    public IActionResult ParseXml([FromBody] XmlRequest request)
    {
        var xmlDoc = new XmlDocument();
        xmlDoc.LoadXml(request.Xml);

        var root = xmlDoc.DocumentElement;
        return Ok(new { Root = root?.OuterXml });
    }

    [HttpGet("config")]
    public IActionResult GetConfig()
    {
        return Ok(new
        {
            AdminPassword,
            ApiSecret,
            DatabaseConnection = "Server=localhost;Database=VulnerableDB;User Id=sa;Password=Admin123!;",
            AwsAccessKey = "AKIAIOSFODNN7EXAMPLE",
            AwsSecretKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        });
    }

    [HttpPost("backup")]
    public IActionResult BackupDatabase([FromBody] BackupRequest request)
    {
        var cmd = $"sqlcmd -S {request.Server} -U sa -P Admin123! -Q \"BACKUP DATABASE {request.Database} TO DISK = '{request.Path}'\"";

        var processInfo = new ProcessStartInfo("cmd.exe", $"/c {cmd}")
        {
            RedirectStandardOutput = true,
            UseShellExecute = false
        };

        using var process = Process.Start(processInfo);
        using var reader = process!.StandardOutput;
        var output = reader.ReadToEnd();

        return Ok(new { Output = output });
    }
}

public record CommandRequest(string Command);
public record PingRequest(string Host);
public record DeserializeRequest(string Data);
public record XmlRequest(string Xml);
public record BackupRequest(string Server, string Database, string Path);
