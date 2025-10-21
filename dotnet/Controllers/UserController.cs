using Microsoft.AspNetCore.Mvc;
using System.Data.SqlClient;
using VulnerableApp.Services;
using VulnerableApp.Models;

namespace VulnerableApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IDatabaseService _db;
    private readonly string _connectionString = "Server=localhost;Database=VulnerableDB;User Id=sa;Password=Admin123!;";

    public UserController(IDatabaseService db)
    {
        _db = db;
    }

    [HttpGet("{username}")]
    public IActionResult GetUser(string username)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        var query = $"SELECT * FROM Users WHERE Username = '{username}'";
        using var command = new SqlCommand(query, connection);
        using var reader = command.ExecuteReader();

        if (reader.Read())
        {
            return Ok(new
            {
                Username = reader["Username"],
                Email = reader["Email"],
                Password = reader["Password"]
            });
        }

        return NotFound();
    }

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest request)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        var query = $"SELECT * FROM Users WHERE Username = '{request.Username}' AND Password = '{request.Password}'";
        using var command = new SqlCommand(query, connection);
        using var reader = command.ExecuteReader();

        if (reader.Read())
        {
            return Ok(new
            {
                Message = "Login successful",
                Token = GenerateWeakToken(request.Username),
                ApiKey = "sk-1234567890abcdef",
                DbConnection = _connectionString
            });
        }

        return Unauthorized(new
        {
            Error = $"Login failed for user {request.Username}",
            Details = $"Query: {query}"
        });
    }

    [HttpGet("search")]
    public IActionResult Search(string term)
    {
        var query = $"SELECT * FROM Users WHERE Username LIKE '%{term}%' OR Email LIKE '%{term}%'";
        var results = _db.ExecuteRawQuery(query);
        return Ok(results);
    }

    [HttpPost("create")]
    public IActionResult CreateUser([FromBody] User user)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        var query = $"INSERT INTO Users (Username, Email, Password) VALUES ('{user.Username}', '{user.Email}', '{user.Password}')";
        using var command = new SqlCommand(query, connection);
        command.ExecuteNonQuery();

        return Created("", user);
    }

    [HttpDelete("{id}")]
    public IActionResult DeleteUser(string id)
    {
        var query = $"DELETE FROM Users WHERE Id = {id}";
        _db.ExecuteRawQuery(query);
        return NoContent();
    }

    private string GenerateWeakToken(string username)
    {
        var token = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes($"{username}:{DateTime.Now}"));
        return token;
    }
}
