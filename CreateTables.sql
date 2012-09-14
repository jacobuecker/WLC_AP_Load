/****** Object:  Table [dbo].[wlc_aps]    Script Date: 09/14/2012 16:21:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[wlc_aps](
	[ap_key] [varchar](200) NOT NULL,
	[ap_name] [varchar](500) NULL,
	[ap_location] [varchar](500) NULL,
 CONSTRAINT [PK_wlc_aps] PRIMARY KEY CLUSTERED 
(
	[ap_key] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[wlc_ap_clients](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[ap_key] [varchar](200) NOT NULL,
	[timestamp] [datetime] NOT NULL,
	[num_of_clients] [int] NOT NULL,
 CONSTRAINT [PK_wlc_ap_clients] PRIMARY KEY CLUSTERED 
(
	[id] ASC,
	[ap_key] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[wlc_ap_clients] ADD  CONSTRAINT [DF_wlc_ap_clients_timestamp]  DEFAULT (getdate()) FOR [timestamp]
GO
