USE [master]
GO
/****** Object:  Database [ADataProInternship]    Script Date: 23/07/2021 10:41:53 ******/
CREATE DATABASE [ADataProInternship]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ADataProInternship', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\ADataProInternship.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ADataProInternship_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\ADataProInternship_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [ADataProInternship] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [ADataProInternship].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [ADataProInternship] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [ADataProInternship] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [ADataProInternship] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [ADataProInternship] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [ADataProInternship] SET ARITHABORT OFF 
GO
ALTER DATABASE [ADataProInternship] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [ADataProInternship] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [ADataProInternship] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [ADataProInternship] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [ADataProInternship] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [ADataProInternship] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [ADataProInternship] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [ADataProInternship] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [ADataProInternship] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [ADataProInternship] SET  DISABLE_BROKER 
GO
ALTER DATABASE [ADataProInternship] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [ADataProInternship] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [ADataProInternship] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [ADataProInternship] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [ADataProInternship] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [ADataProInternship] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [ADataProInternship] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [ADataProInternship] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [ADataProInternship] SET  MULTI_USER 
GO
ALTER DATABASE [ADataProInternship] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [ADataProInternship] SET DB_CHAINING OFF 
GO
ALTER DATABASE [ADataProInternship] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [ADataProInternship] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [ADataProInternship] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [ADataProInternship] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [ADataProInternship] SET QUERY_STORE = OFF
GO
USE [ADataProInternship]
GO
/****** Object:  Table [dbo].[LinkForEachProductInStore]    Script Date: 23/07/2021 10:41:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LinkForEachProductInStore](
	[ProductId] [int] NOT NULL,
	[StoreId] [int] NOT NULL,
	[Link] [nvarchar](400) NOT NULL,
 CONSTRAINT [PK_LinkForEachProductInStore] PRIMARY KEY CLUSTERED 
(
	[ProductId] ASC,
	[StoreId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UQ_LinkForEachProductInStore] UNIQUE NONCLUSTERED 
(
	[Link] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PricesForEachStore]    Script Date: 23/07/2021 10:41:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PricesForEachStore](
	[ProductId] [int] NOT NULL,
	[StoreId] [int] NOT NULL,
	[IsAvailable] [bit] NOT NULL,
	[Price] [real] NULL,
 CONSTRAINT [PK_PricesForEachStore] PRIMARY KEY CLUSTERED 
(
	[ProductId] ASC,
	[StoreId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UQ_PricesForEachStore] UNIQUE NONCLUSTERED 
(
	[ProductId] ASC,
	[StoreId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Products]    Script Date: 23/07/2021 10:41:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Products](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[ProductNumber] [nvarchar](52) NOT NULL,
	[ProductName] [nvarchar](255) NOT NULL,
	[ImgLink] [nvarchar](255) NOT NULL,
 CONSTRAINT [PK__Products__3214EC07F053A0F3] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Stores]    Script Date: 23/07/2021 10:41:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Stores](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[StoreName] [nvarchar](255) NOT NULL,
 CONSTRAINT [PK__Stores__3214EC07485C8D9D] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[LinkForEachProductInStore]  WITH CHECK ADD  CONSTRAINT [FK_LinkForEachProductInStore_Products] FOREIGN KEY([ProductId])
REFERENCES [dbo].[Products] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[LinkForEachProductInStore] CHECK CONSTRAINT [FK_LinkForEachProductInStore_Products]
GO
ALTER TABLE [dbo].[LinkForEachProductInStore]  WITH CHECK ADD  CONSTRAINT [FK_LinkForEachProductInStore_Stores] FOREIGN KEY([StoreId])
REFERENCES [dbo].[Stores] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[LinkForEachProductInStore] CHECK CONSTRAINT [FK_LinkForEachProductInStore_Stores]
GO
ALTER TABLE [dbo].[PricesForEachStore]  WITH CHECK ADD  CONSTRAINT [FK_PriceForEachStore_Products] FOREIGN KEY([ProductId])
REFERENCES [dbo].[Products] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[PricesForEachStore] CHECK CONSTRAINT [FK_PriceForEachStore_Products]
GO
ALTER TABLE [dbo].[PricesForEachStore]  WITH CHECK ADD  CONSTRAINT [FK_PriceForEachStore_Stores] FOREIGN KEY([StoreId])
REFERENCES [dbo].[Stores] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[PricesForEachStore] CHECK CONSTRAINT [FK_PriceForEachStore_Stores]
GO
/****** Object:  StoredProcedure [dbo].[AddProduct]    Script Date: 23/07/2021 10:41:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[AddProduct]
@ProductNumber nvarchar(52),
@ProductName nvarchar(255),
@ProductStore nvarchar(255),
@ImgLink nvarchar(255),
@UrlLink nvarchar(400),
@IsProductAvailable bit,
@ProductPrice real

AS

-- Checks if product number is already taken
IF NOT EXISTS(SELECT ProductNumber FROM Products WHERE ProductNumber = @ProductNumber)
BEGIN
	-- Insert into Products table
	INSERT INTO Products (ProductNumber, ProductName, ImgLink)
	VALUES(@ProductNumber, @ProductName, @ImgLink)
END

-- Checks if there is already a store with this name
IF NOT EXISTS(SELECT StoreName FROM Stores WHERE StoreName = @ProductStore)
BEGIN
	-- Insert into Stores table
	INSERT INTO Stores (StoreName)
	VALUES (@ProductStore)
END

-- Check if there is already a link
IF NOT EXISTS(SELECT Link FROM LinkForEachProductInStore WHERE Link = @UrlLink)
BEGIN
	INSERT INTO LinkForEachProductInStore (ProductId, StoreId, Link)
	SELECT(SELECT Id FROM Products WHERE ProductNumber = @ProductNumber) as ProductId, (SELECT Id FROM Stores WHERE StoreName = @ProductStore) as StoreId, @UrlLink
END

INSERT INTO PricesForEachStore (ProductId, StoreId, IsAvailable, Price)
SELECT(SELECT Id FROM Products WHERE ProductNumber = @ProductNumber) as ProductId, (SELECT Id FROM Stores WHERE StoreName = @ProductStore) as StoreId, @IsProductAvailable, @ProductPrice

SELECT 0 AS ReturnCode
GO
USE [master]
GO
ALTER DATABASE [ADataProInternship] SET  READ_WRITE 
GO
