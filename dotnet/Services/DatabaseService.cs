using System.Data;
using System.Data.SqlClient;

namespace VulnerableApp.Services;

public interface IDatabaseService
{
    DataTable ExecuteRawQuery(string query);
    void ExecuteNonQuery(string query);
}

public class DatabaseService : IDatabaseService
{
    private readonly string _connectionString = "Server=localhost;Database=VulnerableDB;User Id=sa;Password=Admin123!;TrustServerCertificate=true";

    public DataTable ExecuteRawQuery(string query)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        using var command = new SqlCommand(query, connection);
        using var adapter = new SqlDataAdapter(command);

        var dataTable = new DataTable();
        adapter.Fill(dataTable);

        return dataTable;
    }

    public void ExecuteNonQuery(string query)
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        using var command = new SqlCommand(query, connection);
        command.ExecuteNonQuery();
    }
}
