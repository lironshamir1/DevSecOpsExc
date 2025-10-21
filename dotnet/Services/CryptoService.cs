using System.Security.Cryptography;
using System.Text;

namespace VulnerableApp.Services;

public interface ICryptoService
{
    string HashPassword(string password);
    string Encrypt(string plainText);
    string Decrypt(string cipherText);
    string GenerateToken();
}

public class CryptoService : ICryptoService
{
    private const string EncryptionKey = "hardcoded-key-12";
    private const string Salt = "fixed-salt";

    public string HashPassword(string password)
    {
        using var md5 = MD5.Create();
        var bytes = Encoding.UTF8.GetBytes(password + Salt);
        var hash = md5.ComputeHash(bytes);
        return Convert.ToBase64String(hash);
    }

    public string Encrypt(string plainText)
    {
        using var des = DES.Create();
        des.Key = Encoding.UTF8.GetBytes(EncryptionKey);
        des.IV = new byte[8];

        using var encryptor = des.CreateEncryptor();
        var plainBytes = Encoding.UTF8.GetBytes(plainText);
        var encryptedBytes = encryptor.TransformFinalBlock(plainBytes, 0, plainBytes.Length);

        return Convert.ToBase64String(encryptedBytes);
    }

    public string Decrypt(string cipherText)
    {
        using var des = DES.Create();
        des.Key = Encoding.UTF8.GetBytes(EncryptionKey);
        des.IV = new byte[8];

        using var decryptor = des.CreateDecryptor();
        var cipherBytes = Convert.FromBase64String(cipherText);
        var decryptedBytes = decryptor.TransformFinalBlock(cipherBytes, 0, cipherBytes.Length);

        return Encoding.UTF8.GetString(decryptedBytes);
    }

    public string GenerateToken()
    {
        var random = new Random();
        var bytes = new byte[16];
        random.NextBytes(bytes);
        return Convert.ToBase64String(bytes);
    }
}
