from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import KEY_snpsAssociated_FDR

engine = create_engine(KEY_snpsAssociated_FDR)
Sesion = sessionmaker(bind=engine)
Base = declarative_base()
session = Sesion()


class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"
    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))

    def get_SNP_chrom(_id):
        data = session.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        return data[0] if len(data) is 1 else None


def snpsAssociated_FDR_chr_table(chrID):
    class snpsAssociated_FDR_chr(Base):
        __tablename__ = 'snpsAssociated_FDR_{chrID}'.format(chrID=str(chrID))

        chrom = sqlalchemy.Column(String(5))
        chromStart = sqlalchemy.Column(Integer, primary_key=True)
        snpID = sqlalchemy.Column(String(10), primary_key=True)
        chromStartSNP = sqlalchemy.Column(Integer)
        refBase = sqlalchemy.Column(String(2))
        altBase = sqlalchemy.Column(String(2))
        hetero = sqlalchemy.Column(String(2))
        uRefBase = sqlalchemy.Column(Integer)
        uAltBase = sqlalchemy.Column(Integer)
        uHetero = sqlalchemy.Column(Integer)
        mRefBase = sqlalchemy.Column(Integer)
        mAltBase = sqlalchemy.Column(Integer)
        mHetero = sqlalchemy.Column(Integer)
        iRefBase = sqlalchemy.Column(Integer)
        iAltBase = sqlalchemy.Column(Integer)
        iHetero = sqlalchemy.Column(Integer)
        other = sqlalchemy.Column(Integer)
        methCount = sqlalchemy.Column(Integer)
        numSamples = sqlalchemy.Column(Integer)
        pValue = sqlalchemy.Column(Float)
        qValue = sqlalchemy.Column(Float)

        def get_Associated(snpID):
            data = session.query(snpsAssociated_FDR_chr).filter_by(snpID=snpID).all()
            snpsAssociated_FDR_chr.metadata.clear()
            return data

    return snpsAssociated_FDR_chr