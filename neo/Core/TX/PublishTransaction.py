

from neo.Core.TX.Transaction import Transaction,TransactionType
import sys
from neo.Core.FunctionCode import FunctionCode
import binascii
class PublishTransaction(Transaction):


    Code = None
    NeedStorage = False
    Name = ''
    CodeVersion = ''
    Author = ''
    Email = ''
    Description = ''


    def __init__(self, *args, **kwargs):
        super(PublishTransaction, self).__init__(*args, **kwargs)
        self.Type = TransactionType.PublishTransaction


    def DeserializeExclusiveData(self, reader):
        if self.Version > 1:
            self.__log.debug("format exception...")

        self.Code = FunctionCode()
        self.Code.Deserialize(reader)

        if self.Version >= 1:
            self.NeedStorage = reader.ReadBool()
        else:
            self.NeedStorage = False

        self.Name = reader.ReadVarString()
        self.CodeVersion = reader.ReadVarString()
        self.Author = reader.ReadVarString()
        self.Email = reader.ReadVarString()
        self.Description = reader.ReadVarString()



    def SerializePossibleEncodingIssue(self, writer, value):
        length = len(value)
        ba = bytearray(value)
        byts = binascii.hexlify(ba)
        string = byts.decode('utf-8')
        writer.WriteByte(length)
        writer.WriteBytes(string)

    def SerializeExclusiveData(self, writer):

        self.Code.Serialize(writer)

        if self.Version >=1:
            writer.WriteBool( self.NeedStorage)

        self.SerializePossibleEncodingIssue(writer, self.Name)
        self.SerializePossibleEncodingIssue(writer, self.CodeVersion)
        self.SerializePossibleEncodingIssue(writer, self.Author)
        self.SerializePossibleEncodingIssue(writer, self.Email)
        self.SerializePossibleEncodingIssue(writer, self.Description)



    def ToJson(self):
        jsn = super(PublishTransaction, self).ToJson()
        jsn['contract'] = {}
        jsn['contract']['code'] = self.Code.ToJson()
        jsn['contract']['needstorage'] = self.NeedStorage
        jsn['contract']['name'] = self.Name.decode('utf-8')
        jsn['contract']['version'] = self.CodeVersion.decode('utf-8')
        jsn['contract']['author'] = self.Author.decode('utf-8')
        jsn['contract']['email'] = self.Email.decode('utf-8')
        jsn['contract']['description'] = self.Description.decode('utf-8')
        return jsn

#        writer.WriteVarString(self.Name)

#        writer.WriteVarString(self.CodeVersion)
#        writer.WriteVarString(self.Author)
#        writer.WriteVarString(self.Email)


#        self.__log.debug("bytelen: %s " % len(writer.stream.ToArray()))

#        writer.WriteVarBytes(self.Description)
#        self.__log.debug( "bytelen: %s " % len(writer.stream.ToArray()))

