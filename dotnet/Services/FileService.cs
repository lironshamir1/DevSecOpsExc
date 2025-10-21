namespace VulnerableApp.Services;

public interface IFileService
{
    string ReadFile(string path);
    void WriteFile(string path, string content);
    void DeleteFile(string path);
}

public class FileService : IFileService
{
    public string ReadFile(string path)
    {
        return File.ReadAllText(path);
    }

    public void WriteFile(string path, string content)
    {
        File.WriteAllText(path, content);
    }

    public void DeleteFile(string path)
    {
        File.Delete(path);
    }
}
