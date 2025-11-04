FROM mcr.microsoft.com/dotnet/aspnet:8.0

ARG API_KEY=hardcoded-api-key-xyz
ARG DB_PASSWORD=Admin123!

WORKDIR /app

COPY bin/Release/net8.0/publish/ .

ENV ASPNETCORE_URLS=http://+:80
ENV API_KEY=$API_KEY
ENV DB_PASSWORD=$DB_PASSWORD
ENV ASPNETCORE_ENVIRONMENT=Development

RUN chmod 777 /app

EXPOSE 80

ENTRYPOINT ["dotnet", "VulnerableApp.dll"]
