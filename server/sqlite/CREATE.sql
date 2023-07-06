Create Table certifications(
    certName text NOT NULL,
    certId text NOT NULL UNIQUE,
);

Create Table banInstance(
    bannedRobloxId text NOT NULL,
    reporterRobloxId text NOT NULL,

    banReason text NOT NULL,
    banDate text NOT NULL,
    banExpiry text NOT NULL
);

Create Table robloxUser(
    robloxId text NOT NULL UNIQUE,
    is_banned boolean NOT NULL,
    hasDriversLicense boolean NOT NULL
    userCerts text
    FOREIGN KEY(userCerts) REFERENCES certifications(certId)
);