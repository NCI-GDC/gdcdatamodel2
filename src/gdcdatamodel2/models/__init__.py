import sys

from .aggregated_somatic_mutation import AggregatedSomaticMutation
from .aggregatedsomaticmutationdatafromsomaticaggregationworkflow import (
    AggregatedSomaticMutationDataFromSomaticAggregationWorkflow,
)
from .aggregatedsomaticmutationderivedfromproject import (
    AggregatedSomaticMutationDerivedFromProject,
)
from .aggregatedsomaticmutationrelatestocase import (
    AggregatedSomaticMutationRelatesToCase,
)
from .aligned_reads import AlignedReads
from .aligned_reads_index import AlignedReadsIndex
from .alignedreadsdatafromalignmentcocleaningworkflow import (
    AlignedReadsDataFromAlignmentCocleaningWorkflow,
)
from .alignedreadsdatafromalignmentworkflow import AlignedReadsDataFromAlignmentWorkflow
from .alignedreadsindexderivedfromalignedreads import (
    AlignedReadsIndexDerivedFromAlignedReads,
)
from .alignedreadsindexderivedfromsubmittedalignedreads import (
    AlignedReadsIndexDerivedFromSubmittedAlignedReads,
)
from .alignedreadsindexrelatestocase import AlignedReadsIndexRelatesToCase
from .alignedreadsmatchedtosubmittedalignedreads import (
    AlignedReadsMatchedToSubmittedAlignedReads,
)
from .alignedreadsmatchedtosubmittedunalignedreads import (
    AlignedReadsMatchedToSubmittedUnalignedReads,
)
from .alignedreadsrelatestocase import AlignedReadsRelatesToCase
from .alignment_cocleaning_workflow import AlignmentCocleaningWorkflow
from .alignment_workflow import AlignmentWorkflow
from .alignmentcocleaningworkflowperformedonsubmittedalignedreads import (
    AlignmentCocleaningWorkflowPerformedOnSubmittedAlignedReads,
)
from .alignmentcocleaningworkflowperformedonsubmittedunalignedreads import (
    AlignmentCocleaningWorkflowPerformedOnSubmittedUnalignedReads,
)
from .alignmentcocleaningworkflowrelatestocase import (
    AlignmentCocleaningWorkflowRelatesToCase,
)
from .alignmentworkflowperformedonsubmittedalignedreads import (
    AlignmentWorkflowPerformedOnSubmittedAlignedReads,
)
from .alignmentworkflowperformedonsubmittedunalignedreads import (
    AlignmentWorkflowPerformedOnSubmittedUnalignedReads,
)
from .alignmentworkflowrelatestocase import AlignmentWorkflowRelatesToCase
from .aliquot import Aliquot
from .aliquotderivedfromanalyte import AliquotDerivedFromAnalyte
from .aliquotderivedfromsample import AliquotDerivedFromSample
from .aliquotrelatestocase import AliquotRelatesToCase
from .aliquotshippedtocenter import AliquotShippedToCenter
from .analysis_metadata import AnalysisMetadata
from .analysismetadataderivedfromfile import AnalysisMetadataDerivedFromFile
from .analysismetadataderivedfromsubmittedalignedreads import (
    AnalysisMetadataDerivedFromSubmittedAlignedReads,
)
from .analysismetadatarelatestocase import AnalysisMetadataRelatesToCase
from .analyte import Analyte
from .analytederivedfromportion import AnalyteDerivedFromPortion
from .analytederivedfromsample import AnalyteDerivedFromSample
from .analyterelatestocase import AnalyteRelatesToCase
from .annotated_somatic_mutation import AnnotatedSomaticMutation
from .annotatedsomaticmutationdatafromgenomicprofileharmonizationworkflow import (
    AnnotatedSomaticMutationDataFromGenomicProfileHarmonizationWorkflow,
)
from .annotatedsomaticmutationdatafromsomaticannotationworkflow import (
    AnnotatedSomaticMutationDataFromSomaticAnnotationWorkflow,
)
from .annotatedsomaticmutationrelatestocase import AnnotatedSomaticMutationRelatesToCase
from .annotation import Annotation
from .annotationannotatesaggregatedsomaticmutation import (
    AnnotationAnnotatesAggregatedSomaticMutation,
)
from .annotationannotatesalignedreads import AnnotationAnnotatesAlignedReads
from .annotationannotatesalignedreadsindex import AnnotationAnnotatesAlignedReadsIndex
from .annotationannotatesaliquot import AnnotationAnnotatesAliquot
from .annotationannotatesanalysismetadata import AnnotationAnnotatesAnalysisMetadata
from .annotationannotatesanalyte import AnnotationAnnotatesAnalyte
from .annotationannotatesannotatedsomaticmutation import (
    AnnotationAnnotatesAnnotatedSomaticMutation,
)
from .annotationannotatesarchive import AnnotationAnnotatesArchive
from .annotationannotatesbiospecimensupplement import (
    AnnotationAnnotatesBiospecimenSupplement,
)
from .annotationannotatescase import AnnotationAnnotatesCase
from .annotationannotatescenter import AnnotationAnnotatesCenter
from .annotationannotatesclinicalsupplement import AnnotationAnnotatesClinicalSupplement
from .annotationannotatescopynumberauxiliaryfile import (
    AnnotationAnnotatesCopyNumberAuxiliaryFile,
)
from .annotationannotatescopynumberestimate import AnnotationAnnotatesCopyNumberEstimate
from .annotationannotatescopynumbersegment import AnnotationAnnotatesCopyNumberSegment
from .annotationannotatesdemographic import AnnotationAnnotatesDemographic
from .annotationannotatesdiagnosis import AnnotationAnnotatesDiagnosis
from .annotationannotatesexperimentmetadata import AnnotationAnnotatesExperimentMetadata
from .annotationannotatesexposure import AnnotationAnnotatesExposure
from .annotationannotatesfamilyhistory import AnnotationAnnotatesFamilyHistory
from .annotationannotatesfile import AnnotationAnnotatesFile
from .annotationannotatesfilteredcopynumbersegment import (
    AnnotationAnnotatesFilteredCopyNumberSegment,
)
from .annotationannotatesfollowup import AnnotationAnnotatesFollowUp
from .annotationannotatesgeneexpression import AnnotationAnnotatesGeneExpression
from .annotationannotatesmaskedmethylationarray import (
    AnnotationAnnotatesMaskedMethylationArray,
)
from .annotationannotatesmaskedsomaticmutation import (
    AnnotationAnnotatesMaskedSomaticMutation,
)
from .annotationannotatesmethylationbetavalue import (
    AnnotationAnnotatesMethylationBetaValue,
)
from .annotationannotatesmirnaexpression import AnnotationAnnotatesMirnaExpression
from .annotationannotatesmoleculartest import AnnotationAnnotatesMolecularTest
from .annotationannotatesotherclinicalattribute import (
    AnnotationAnnotatesOtherClinicalAttribute,
)
from .annotationannotatespathologydetail import AnnotationAnnotatesPathologyDetail
from .annotationannotatespathologyreport import AnnotationAnnotatesPathologyReport
from .annotationannotatesportion import AnnotationAnnotatesPortion
from .annotationannotatesproteinexpression import AnnotationAnnotatesProteinExpression
from .annotationannotatesrawmethylationarray import (
    AnnotationAnnotatesRawMethylationArray,
)
from .annotationannotatesreadgroup import AnnotationAnnotatesReadGroup
from .annotationannotatesreadgroupqc import AnnotationAnnotatesReadGroupQc
from .annotationannotatesrunmetadata import AnnotationAnnotatesRunMetadata
from .annotationannotatessample import AnnotationAnnotatesSample
from .annotationannotatessecondaryexpressionanalysis import (
    AnnotationAnnotatesSecondaryExpressionAnalysis,
)
from .annotationannotatessimplegermlinevariation import (
    AnnotationAnnotatesSimpleGermlineVariation,
)
from .annotationannotatessimplesomaticmutation import (
    AnnotationAnnotatesSimpleSomaticMutation,
)
from .annotationannotatesslide import AnnotationAnnotatesSlide
from .annotationannotatesslideimage import AnnotationAnnotatesSlideImage
from .annotationannotatessomaticmutationindex import (
    AnnotationAnnotatesSomaticMutationIndex,
)
from .annotationannotatesstructuralvariation import (
    AnnotationAnnotatesStructuralVariation,
)
from .annotationannotatessubmittedalignedreads import (
    AnnotationAnnotatesSubmittedAlignedReads,
)
from .annotationannotatessubmittedgenomicprofile import (
    AnnotationAnnotatesSubmittedGenomicProfile,
)
from .annotationannotatessubmittedgenotypingarray import (
    AnnotationAnnotatesSubmittedGenotypingArray,
)
from .annotationannotatessubmittedmethylationbetavalue import (
    AnnotationAnnotatesSubmittedMethylationBetaValue,
)
from .annotationannotatessubmittedtangentcopynumber import (
    AnnotationAnnotatesSubmittedTangentCopyNumber,
)
from .annotationannotatessubmittedunalignedreads import (
    AnnotationAnnotatesSubmittedUnalignedReads,
)
from .annotationannotatestissuesourcesite import AnnotationAnnotatesTissueSourceSite
from .annotationannotatestreatment import AnnotationAnnotatesTreatment
from .annotationrelatestocase import AnnotationRelatesToCase
from .archive import Archive
from .archivememberofproject import ArchiveMemberOfProject
from .archiverelatedtofile import ArchiveRelatedToFile
from .archiverelatestocase import ArchiveRelatesToCase
from .biospecimen_supplement import BiospecimenSupplement
from .biospecimensupplementderivedfromcase import BiospecimenSupplementDerivedFromCase
from .biospecimensupplementmemberofarchive import BiospecimenSupplementMemberOfArchive
from .biospecimensupplementrelatestocase import BiospecimenSupplementRelatesToCase
from .case import Case
from .casememberofproject import CaseMemberOfProject
from .caseprocessedattissuesourcesite import CaseProcessedAtTissueSourceSite
from .center import Center
from .clinical import Clinical
from .clinical_supplement import ClinicalSupplement
from .clinicaldescribescase import ClinicalDescribesCase
from .clinicalrelatestocase import ClinicalRelatesToCase
from .clinicalsupplementderivedfromcase import ClinicalSupplementDerivedFromCase
from .clinicalsupplementmemberofarchive import ClinicalSupplementMemberOfArchive
from .clinicalsupplementrelatestocase import ClinicalSupplementRelatesToCase
from .copy_number_auxiliary_file import CopyNumberAuxiliaryFile
from .copy_number_estimate import CopyNumberEstimate
from .copy_number_liftover_workflow import CopyNumberLiftoverWorkflow
from .copy_number_segment import CopyNumberSegment
from .copy_number_variation_workflow import CopyNumberVariationWorkflow
from .copynumberauxiliaryfilederivedfromsomaticcopynumberworkflow import (
    CopyNumberAuxiliaryFileDerivedFromSomaticCopyNumberWorkflow,
)
from .copynumberauxiliaryfilerelatestocase import CopyNumberAuxiliaryFileRelatesToCase
from .copynumberestimatederivedfromcopynumbervariationworkflow import (
    CopyNumberEstimateDerivedFromCopyNumberVariationWorkflow,
)
from .copynumberestimatederivedfromgenomicprofileharmonizationworkflow import (
    CopyNumberEstimateDerivedFromGenomicProfileHarmonizationWorkflow,
)
from .copynumberestimatederivedfromsomaticcopynumberworkflow import (
    CopyNumberEstimateDerivedFromSomaticCopyNumberWorkflow,
)
from .copynumberestimaterelatestocase import CopyNumberEstimateRelatesToCase
from .copynumberliftoverworkflowperformedonsubmittedtangentcopynumber import (
    CopyNumberLiftoverWorkflowPerformedOnSubmittedTangentCopyNumber,
)
from .copynumberliftoverworkflowrelatestocase import (
    CopyNumberLiftoverWorkflowRelatesToCase,
)
from .copynumbersegmentderivedfromcopynumberliftoverworkflow import (
    CopyNumberSegmentDerivedFromCopyNumberLiftoverWorkflow,
)
from .copynumbersegmentderivedfromgenomicprofileharmonizationworkflow import (
    CopyNumberSegmentDerivedFromGenomicProfileHarmonizationWorkflow,
)
from .copynumbersegmentderivedfromsomaticcopynumberworkflow import (
    CopyNumberSegmentDerivedFromSomaticCopyNumberWorkflow,
)
from .copynumbersegmentrelatestocase import CopyNumberSegmentRelatesToCase
from .copynumbervariationworkflowperformedoncopynumbersegment import (
    CopyNumberVariationWorkflowPerformedOnCopyNumberSegment,
)
from .copynumbervariationworkflowrelatestocase import (
    CopyNumberVariationWorkflowRelatesToCase,
)
from .data_format import DataFormat
from .data_release import DataRelease
from .data_subtype import DataSubtype
from .data_type import DataType
from .datareleasedescribesroot import DataReleaseDescribesRoot
from .datareleaserelatestocase import DataReleaseRelatesToCase
from .datasubtypememberofdatatype import DataSubtypeMemberOfDataType
from .demographic import Demographic
from .demographicdescribescase import DemographicDescribesCase
from .demographicrelatestocase import DemographicRelatesToCase
from .diagnosis import Diagnosis
from .diagnosisdescribescase import DiagnosisDescribesCase
from .diagnosisrelatestocase import DiagnosisRelatesToCase
from .experiment_metadata import ExperimentMetadata
from .experimental_strategy import ExperimentalStrategy
from .experimentmetadataderivedfromfile import ExperimentMetadataDerivedFromFile
from .experimentmetadataderivedfromreadgroup import (
    ExperimentMetadataDerivedFromReadGroup,
)
from .experimentmetadatarelatestocase import ExperimentMetadataRelatesToCase
from .exposure import Exposure
from .exposuredescribescase import ExposureDescribesCase
from .exposurerelatestocase import ExposureRelatesToCase
from .expression_analysis_workflow import ExpressionAnalysisWorkflow
from .expressionanalysisworkflowperformedongeneexpression import (
    ExpressionAnalysisWorkflowPerformedOnGeneExpression,
)
from .expressionanalysisworkflowrelatestocase import (
    ExpressionAnalysisWorkflowRelatesToCase,
)
from .family_history import FamilyHistory
from .familyhistorydescribescase import FamilyHistoryDescribesCase
from .familyhistoryrelatestocase import FamilyHistoryRelatesToCase
from .file import File
from .filedatafromaliquot import FileDataFromAliquot
from .filedatafromanalyte import FileDataFromAnalyte
from .filedatafromcase import FileDataFromCase
from .filedatafromfile import FileDataFromFile
from .filedatafromportion import FileDataFromPortion
from .filedatafromsample import FileDataFromSample
from .filedatafromslide import FileDataFromSlide
from .filedescribescase import FileDescribesCase
from .filegeneratedfromplatform import FileGeneratedFromPlatform
from .filememberofarchive import FileMemberOfArchive
from .filememberofdataformat import FileMemberOfDataFormat
from .filememberofdatasubtype import FileMemberOfDataSubtype
from .filememberofexperimentalstrategy import FileMemberOfExperimentalStrategy
from .filememeberoftag import FileMemeberOfTag
from .filerelatedtofile import FileRelatedToFile
from .filerelatestocase import FileRelatesToCase
from .filesubmittedbycenter import FileSubmittedByCenter
from .filtered_copy_number_segment import FilteredCopyNumberSegment
from .filteredcopynumbersegmentdatafromcopynumberliftoverworkflow import (
    FilteredCopyNumberSegmentDataFromCopyNumberLiftoverWorkflow,
)
from .filteredcopynumbersegmentrelatestocase import (
    FilteredCopyNumberSegmentRelatesToCase,
)
from .follow_up import FollowUp
from .followupdescribescase import FollowUpDescribesCase
from .followupdescribesdiagnosis import FollowUpDescribesDiagnosis
from .followuprelatestocase import FollowUpRelatesToCase
from .gene_expression import GeneExpression
from .geneexpressiondatafromrnaexpressionworkflow import (
    GeneExpressionDataFromRnaExpressionWorkflow,
)
from .geneexpressionrelatestocase import GeneExpressionRelatesToCase
from .genomic_profile_harmonization_workflow import GenomicProfileHarmonizationWorkflow
from .genomicprofileharmonizationworkflowperformedonsubmittedgenomicprofile import (
    GenomicProfileHarmonizationWorkflowPerformedOnSubmittedGenomicProfile,
)
from .genomicprofileharmonizationworkflowrelatestocase import (
    GenomicProfileHarmonizationWorkflowRelatesToCase,
)
from .germline_mutation_calling_workflow import GermlineMutationCallingWorkflow
from .germlinemutationcallingworkflowperformedonalignedreads import (
    GermlineMutationCallingWorkflowPerformedOnAlignedReads,
)
from .germlinemutationcallingworkflowperformedonsubmittedgenotypingarray import (
    GermlineMutationCallingWorkflowPerformedOnSubmittedGenotypingArray,
)
from .germlinemutationcallingworkflowrelatestocase import (
    GermlineMutationCallingWorkflowRelatesToCase,
)
from .helpers import base, indexes, related_cases, versioned_nodes, versioning
from .masked_methylation_array import MaskedMethylationArray
from .masked_somatic_mutation import MaskedSomaticMutation
from .maskedmethylationarraydatafrommethylationarrayharmonizationworkflow import (
    MaskedMethylationArrayDataFromMethylationArrayHarmonizationWorkflow,
)
from .maskedmethylationarrayrelatestocase import MaskedMethylationArrayRelatesToCase
from .maskedsomaticmutationdatafromgenomicprofileharmonizationworkflow import (
    MaskedSomaticMutationDataFromGenomicProfileHarmonizationWorkflow,
)
from .maskedsomaticmutationdatafromsomaticaggregationworkflow import (
    MaskedSomaticMutationDataFromSomaticAggregationWorkflow,
)
from .maskedsomaticmutationderivedfromproject import (
    MaskedSomaticMutationDerivedFromProject,
)
from .maskedsomaticmutationrelatestocase import MaskedSomaticMutationRelatesToCase
from .methylation_array_harmonization_workflow import (
    MethylationArrayHarmonizationWorkflow,
)
from .methylation_beta_value import MethylationBetaValue
from .methylation_liftover_workflow import MethylationLiftoverWorkflow
from .methylationarrayharmonizationworkflowperformedonrawmethylationarray import (
    MethylationArrayHarmonizationWorkflowPerformedOnRawMethylationArray,
)
from .methylationarrayharmonizationworkflowrelatestocase import (
    MethylationArrayHarmonizationWorkflowRelatesToCase,
)
from .methylationbetavaluedatafrommethylationarrayharmonizationworkflow import (
    MethylationBetaValueDataFromMethylationArrayHarmonizationWorkflow,
)
from .methylationbetavaluedatafrommethylationliftoverworkflow import (
    MethylationBetaValueDataFromMethylationLiftoverWorkflow,
)
from .methylationbetavaluerelatestocase import MethylationBetaValueRelatesToCase
from .methylationliftoverworkflowperformedonsubmittedmethylationbetavalue import (
    MethylationLiftoverWorkflowPerformedOnSubmittedMethylationBetaValue,
)
from .methylationliftoverworkflowrelatestocase import (
    MethylationLiftoverWorkflowRelatesToCase,
)
from .mirna_expression import MirnaExpression
from .mirna_expression_workflow import MirnaExpressionWorkflow
from .mirnaexpressiondatafrommirnaexpressionworkflow import (
    MirnaExpressionDataFromMirnaExpressionWorkflow,
)
from .mirnaexpressionrelatestocase import MirnaExpressionRelatesToCase
from .mirnaexpressionworkflowperformedonalignedreads import (
    MirnaExpressionWorkflowPerformedOnAlignedReads,
)
from .mirnaexpressionworkflowrelatestocase import MirnaExpressionWorkflowRelatesToCase
from .molecular_test import MolecularTest
from .moleculartestperformedatfollowup import MolecularTestPerformedAtFollowUp
from .moleculartestrelatedtodiagnosis import MolecularTestRelatedToDiagnosis
from .moleculartestrelatedtoslide import MolecularTestRelatedToSlide
from .moleculartestrelatestocase import MolecularTestRelatesToCase
from .other_clinical_attribute import OtherClinicalAttribute
from .otherclinicalattributedescribescase import OtherClinicalAttributeDescribesCase
from .otherclinicalattributedescribesfollowup import (
    OtherClinicalAttributeDescribesFollowUp,
)
from .otherclinicalattributerelatestocase import OtherClinicalAttributeRelatesToCase
from .pathology_detail import PathologyDetail
from .pathology_report import PathologyReport
from .pathologydetaildescribesdiagnosis import PathologyDetailDescribesDiagnosis
from .pathologydetailrelatestocase import PathologyDetailRelatesToCase
from .pathologyreportderivedfromsample import PathologyReportDerivedFromSample
from .pathologyreportrelatestocase import PathologyReportRelatesToCase
from .platform import Platform
from .portion import Portion
from .portionderivedfromsample import PortionDerivedFromSample
from .portionrelatestocase import PortionRelatesToCase
from .portionshippedtocenter import PortionShippedToCenter
from .program import Program
from .project import Project
from .projectmemberofprogram import ProjectMemberOfProgram
from .protein_expression import ProteinExpression
from .proteinexpressionderivedfromportion import ProteinExpressionDerivedFromPortion
from .proteinexpressionderivedfromsample import ProteinExpressionDerivedFromSample
from .proteinexpressionrelatestocase import ProteinExpressionRelatesToCase
from .publication import Publication
from .publicationreferstofile import PublicationRefersToFile
from .raw_methylation_array import RawMethylationArray
from .rawmethylationarraydatafromaliquot import RawMethylationArrayDataFromAliquot
from .rawmethylationarrayrelatestocase import RawMethylationArrayRelatesToCase
from .read_group import ReadGroup
from .read_group_qc import ReadGroupQc
from .readgroupderivedfromaliquot import ReadGroupDerivedFromAliquot
from .readgroupqcdatafromsubmittedalignedreads import (
    ReadGroupQcDataFromSubmittedAlignedReads,
)
from .readgroupqcdatafromsubmittedunalignedreads import (
    ReadGroupQcDataFromSubmittedUnalignedReads,
)
from .readgroupqcgeneratedfromreadgroup import ReadGroupQcGeneratedFromReadGroup
from .readgroupqcrelatestocase import ReadGroupQcRelatesToCase
from .readgrouprelatestocase import ReadGroupRelatesToCase
from .rna_expression_workflow import RnaExpressionWorkflow
from .rnaexpressionworkflowperformedonalignedreads import (
    RnaExpressionWorkflowPerformedOnAlignedReads,
)
from .rnaexpressionworkflowperformedonsubmittedalignedreads import (
    RnaExpressionWorkflowPerformedOnSubmittedAlignedReads,
)
from .rnaexpressionworkflowperformedonsubmittedunalignedreads import (
    RnaExpressionWorkflowPerformedOnSubmittedUnalignedReads,
)
from .rnaexpressionworkflowrelatestocase import RnaExpressionWorkflowRelatesToCase
from .root import Root
from .rootrelatestocase import RootRelatesToCase
from .run_metadata import RunMetadata
from .runmetadataderivedfromfile import RunMetadataDerivedFromFile
from .runmetadataderivedfromreadgroup import RunMetadataDerivedFromReadGroup
from .runmetadatarelatestocase import RunMetadataRelatesToCase
from .sample import Sample
from .samplederivedfromcase import SampleDerivedFromCase
from .samplederivedfromsample import SampleDerivedFromSample
from .sampleprocessedattissuesourcesite import SampleProcessedAtTissueSourceSite
from .samplerelatedtodiagnosis import SampleRelatedToDiagnosis
from .samplerelatestocase import SampleRelatesToCase
from .secondary_expression_analysis import SecondaryExpressionAnalysis
from .secondaryexpressionanalysisdatafromexpressionanalysisworkflow import (
    SecondaryExpressionAnalysisDataFromExpressionAnalysisWorkflow,
)
from .secondaryexpressionanalysisrelatestocase import (
    SecondaryExpressionAnalysisRelatesToCase,
)
from .simple_germline_variation import SimpleGermlineVariation
from .simple_somatic_mutation import SimpleSomaticMutation
from .simplegermlinevariationdatafromgermlinemutationcallingworkflow import (
    SimpleGermlineVariationDataFromGermlineMutationCallingWorkflow,
)
from .simplegermlinevariationrelatestocase import SimpleGermlineVariationRelatesToCase
from .simplesomaticmutationdatafromgenomicprofileharmonizationworkflow import (
    SimpleSomaticMutationDataFromGenomicProfileHarmonizationWorkflow,
)
from .simplesomaticmutationdatafromsomaticmutationcallingworkflow import (
    SimpleSomaticMutationDataFromSomaticMutationCallingWorkflow,
)
from .simplesomaticmutationrelatestocase import SimpleSomaticMutationRelatesToCase
from .slide import Slide
from .slide_image import SlideImage
from .slidederivedfromportion import SlideDerivedFromPortion
from .slidederivedfromsample import SlideDerivedFromSample
from .slideimagedatafromslide import SlideImageDataFromSlide
from .slideimagerelatestocase import SlideImageRelatesToCase
from .sliderelatestocase import SlideRelatesToCase
from .somatic_aggregation_workflow import SomaticAggregationWorkflow
from .somatic_annotation_workflow import SomaticAnnotationWorkflow
from .somatic_copy_number_workflow import SomaticCopyNumberWorkflow
from .somatic_mutation_calling_workflow import SomaticMutationCallingWorkflow
from .somatic_mutation_index import SomaticMutationIndex
from .somaticaggregationworkflowperformedonannotatedsomaticmutation import (
    SomaticAggregationWorkflowPerformedOnAnnotatedSomaticMutation,
)
from .somaticaggregationworkflowperformedonsimplesomaticmutation import (
    SomaticAggregationWorkflowPerformedOnSimpleSomaticMutation,
)
from .somaticaggregationworkflowrelatestocase import (
    SomaticAggregationWorkflowRelatesToCase,
)
from .somaticannotationworkflowperformedonsimplesomaticmutation import (
    SomaticAnnotationWorkflowPerformedOnSimpleSomaticMutation,
)
from .somaticannotationworkflowrelatestocase import (
    SomaticAnnotationWorkflowRelatesToCase,
)
from .somaticcopynumberworkflowperformedonalignedreads import (
    SomaticCopyNumberWorkflowPerformedOnAlignedReads,
)
from .somaticcopynumberworkflowperformedonsubmittedgenotypingarray import (
    SomaticCopyNumberWorkflowPerformedOnSubmittedGenotypingArray,
)
from .somaticcopynumberworkflowrelatestocase import (
    SomaticCopyNumberWorkflowRelatesToCase,
)
from .somaticmutationcallingworkflowperformedonalignedreads import (
    SomaticMutationCallingWorkflowPerformedOnAlignedReads,
)
from .somaticmutationcallingworkflowrelatestocase import (
    SomaticMutationCallingWorkflowRelatesToCase,
)
from .somaticmutationindexderivedfromannotatedsomaticmutation import (
    SomaticMutationIndexDerivedFromAnnotatedSomaticMutation,
)
from .somaticmutationindexderivedfromsimplesomaticmutation import (
    SomaticMutationIndexDerivedFromSimpleSomaticMutation,
)
from .somaticmutationindexderivedfromstructuralvariation import (
    SomaticMutationIndexDerivedFromStructuralVariation,
)
from .somaticmutationindexrelatestocase import SomaticMutationIndexRelatesToCase
from .structural_variant_calling_workflow import StructuralVariantCallingWorkflow
from .structural_variation import StructuralVariation
from .structuralvariantcallingworkflowperformedonalignedreads import (
    StructuralVariantCallingWorkflowPerformedOnAlignedReads,
)
from .structuralvariantcallingworkflowrelatestocase import (
    StructuralVariantCallingWorkflowRelatesToCase,
)
from .structuralvariationdatafromgenomicprofileharmonizationworkflow import (
    StructuralVariationDataFromGenomicProfileHarmonizationWorkflow,
)
from .structuralvariationdatafromstructuralvariantcallingworkflow import (
    StructuralVariationDataFromStructuralVariantCallingWorkflow,
)
from .structuralvariationrelatestocase import StructuralVariationRelatesToCase
from .submitted_aligned_reads import SubmittedAlignedReads
from .submitted_genomic_profile import SubmittedGenomicProfile
from .submitted_genotyping_array import SubmittedGenotypingArray
from .submitted_methylation_beta_value import SubmittedMethylationBetaValue
from .submitted_tangent_copy_number import SubmittedTangentCopyNumber
from .submitted_unaligned_reads import SubmittedUnalignedReads
from .submittedalignedreadsdatafromreadgroup import (
    SubmittedAlignedReadsDataFromReadGroup,
)
from .submittedalignedreadsrelatestocase import SubmittedAlignedReadsRelatesToCase
from .submittedgenomicprofiledatafromreadgroup import (
    SubmittedGenomicProfileDataFromReadGroup,
)
from .submittedgenomicprofilerelatestocase import SubmittedGenomicProfileRelatesToCase
from .submittedgenotypingarrayderivedfromaliquot import (
    SubmittedGenotypingArrayDerivedFromAliquot,
)
from .submittedgenotypingarrayrelatestocase import SubmittedGenotypingArrayRelatesToCase
from .submittedmethylationbetavaluederivedfromaliquot import (
    SubmittedMethylationBetaValueDerivedFromAliquot,
)
from .submittedmethylationbetavaluerelatestocase import (
    SubmittedMethylationBetaValueRelatesToCase,
)
from .submittedtangentcopynumberderivedfromaliquot import (
    SubmittedTangentCopyNumberDerivedFromAliquot,
)
from .submittedtangentcopynumberrelatestocase import (
    SubmittedTangentCopyNumberRelatesToCase,
)
from .submittedunalignedreadsdatafromreadgroup import (
    SubmittedUnalignedReadsDataFromReadGroup,
)
from .submittedunalignedreadsrelatestocase import SubmittedUnalignedReadsRelatesToCase
from .tag import Tag
from .tissue_source_site import TissueSourceSite
from .treatment import Treatment
from .treatmentdescribesdiagnosis import TreatmentDescribesDiagnosis
from .treatmentrelatestocase import TreatmentRelatesToCase

namespace = base.namespace
Node = base.Node
Edge = base.Edge

__all__ = [
    "AggregatedSomaticMutation",
    "AggregatedSomaticMutationDataFromSomaticAggregationWorkflow",
    "AggregatedSomaticMutationDerivedFromProject",
    "AggregatedSomaticMutationRelatesToCase",
    "AlignedReads",
    "AlignedReadsIndex",
    "AlignedReadsDataFromAlignmentCocleaningWorkflow",
    "AlignedReadsDataFromAlignmentWorkflow",
    "AlignedReadsIndexDerivedFromAlignedReads",
    "AlignedReadsIndexDerivedFromSubmittedAlignedReads",
    "AlignedReadsIndexRelatesToCase",
    "AlignedReadsMatchedToSubmittedAlignedReads",
    "AlignedReadsMatchedToSubmittedUnalignedReads",
    "AlignedReadsRelatesToCase",
    "AlignmentCocleaningWorkflow",
    "AlignmentWorkflow",
    "AlignmentCocleaningWorkflowPerformedOnSubmittedAlignedReads",
    "AlignmentCocleaningWorkflowPerformedOnSubmittedUnalignedReads",
    "AlignmentCocleaningWorkflowRelatesToCase",
    "AlignmentWorkflowPerformedOnSubmittedAlignedReads",
    "AlignmentWorkflowPerformedOnSubmittedUnalignedReads",
    "AlignmentWorkflowRelatesToCase",
    "Aliquot",
    "AliquotDerivedFromAnalyte",
    "AliquotDerivedFromSample",
    "AliquotRelatesToCase",
    "AliquotShippedToCenter",
    "AnalysisMetadata",
    "AnalysisMetadataDerivedFromFile",
    "AnalysisMetadataDerivedFromSubmittedAlignedReads",
    "AnalysisMetadataRelatesToCase",
    "Analyte",
    "AnalyteDerivedFromPortion",
    "AnalyteDerivedFromSample",
    "AnalyteRelatesToCase",
    "AnnotatedSomaticMutation",
    "AnnotatedSomaticMutationDataFromGenomicProfileHarmonizationWorkflow",
    "AnnotatedSomaticMutationDataFromSomaticAnnotationWorkflow",
    "AnnotatedSomaticMutationRelatesToCase",
    "Annotation",
    "AnnotationAnnotatesAggregatedSomaticMutation",
    "AnnotationAnnotatesAlignedReads",
    "AnnotationAnnotatesAlignedReadsIndex",
    "AnnotationAnnotatesAliquot",
    "AnnotationAnnotatesAnalysisMetadata",
    "AnnotationAnnotatesAnalyte",
    "AnnotationAnnotatesAnnotatedSomaticMutation",
    "AnnotationAnnotatesArchive",
    "AnnotationAnnotatesBiospecimenSupplement",
    "AnnotationAnnotatesCase",
    "AnnotationAnnotatesCenter",
    "AnnotationAnnotatesClinicalSupplement",
    "AnnotationAnnotatesCopyNumberAuxiliaryFile",
    "AnnotationAnnotatesCopyNumberEstimate",
    "AnnotationAnnotatesCopyNumberSegment",
    "AnnotationAnnotatesDemographic",
    "AnnotationAnnotatesDiagnosis",
    "AnnotationAnnotatesExperimentMetadata",
    "AnnotationAnnotatesExposure",
    "AnnotationAnnotatesFamilyHistory",
    "AnnotationAnnotatesFile",
    "AnnotationAnnotatesFilteredCopyNumberSegment",
    "AnnotationAnnotatesFollowUp",
    "AnnotationAnnotatesGeneExpression",
    "AnnotationAnnotatesMaskedMethylationArray",
    "AnnotationAnnotatesMaskedSomaticMutation",
    "AnnotationAnnotatesMethylationBetaValue",
    "AnnotationAnnotatesMirnaExpression",
    "AnnotationAnnotatesMolecularTest",
    "AnnotationAnnotatesOtherClinicalAttribute",
    "AnnotationAnnotatesPathologyDetail",
    "AnnotationAnnotatesPathologyReport",
    "AnnotationAnnotatesPortion",
    "AnnotationAnnotatesProteinExpression",
    "AnnotationAnnotatesRawMethylationArray",
    "AnnotationAnnotatesReadGroup",
    "AnnotationAnnotatesReadGroupQc",
    "AnnotationAnnotatesRunMetadata",
    "AnnotationAnnotatesSample",
    "AnnotationAnnotatesSecondaryExpressionAnalysis",
    "AnnotationAnnotatesSimpleGermlineVariation",
    "AnnotationAnnotatesSimpleSomaticMutation",
    "AnnotationAnnotatesSlide",
    "AnnotationAnnotatesSlideImage",
    "AnnotationAnnotatesSomaticMutationIndex",
    "AnnotationAnnotatesStructuralVariation",
    "AnnotationAnnotatesSubmittedAlignedReads",
    "AnnotationAnnotatesSubmittedGenomicProfile",
    "AnnotationAnnotatesSubmittedGenotypingArray",
    "AnnotationAnnotatesSubmittedMethylationBetaValue",
    "AnnotationAnnotatesSubmittedTangentCopyNumber",
    "AnnotationAnnotatesSubmittedUnalignedReads",
    "AnnotationAnnotatesTissueSourceSite",
    "AnnotationAnnotatesTreatment",
    "AnnotationRelatesToCase",
    "Archive",
    "ArchiveMemberOfProject",
    "ArchiveRelatedToFile",
    "ArchiveRelatesToCase",
    "BiospecimenSupplement",
    "BiospecimenSupplementDerivedFromCase",
    "BiospecimenSupplementMemberOfArchive",
    "BiospecimenSupplementRelatesToCase",
    "Case",
    "CaseMemberOfProject",
    "CaseProcessedAtTissueSourceSite",
    "Center",
    "Clinical",
    "ClinicalSupplement",
    "ClinicalDescribesCase",
    "ClinicalRelatesToCase",
    "ClinicalSupplementDerivedFromCase",
    "ClinicalSupplementMemberOfArchive",
    "ClinicalSupplementRelatesToCase",
    "CopyNumberAuxiliaryFile",
    "CopyNumberEstimate",
    "CopyNumberLiftoverWorkflow",
    "CopyNumberSegment",
    "CopyNumberVariationWorkflow",
    "CopyNumberAuxiliaryFileDerivedFromSomaticCopyNumberWorkflow",
    "CopyNumberAuxiliaryFileRelatesToCase",
    "CopyNumberEstimateDerivedFromCopyNumberVariationWorkflow",
    "CopyNumberEstimateDerivedFromGenomicProfileHarmonizationWorkflow",
    "CopyNumberEstimateDerivedFromSomaticCopyNumberWorkflow",
    "CopyNumberEstimateRelatesToCase",
    "CopyNumberLiftoverWorkflowPerformedOnSubmittedTangentCopyNumber",
    "CopyNumberLiftoverWorkflowRelatesToCase",
    "CopyNumberSegmentDerivedFromCopyNumberLiftoverWorkflow",
    "CopyNumberSegmentDerivedFromGenomicProfileHarmonizationWorkflow",
    "CopyNumberSegmentDerivedFromSomaticCopyNumberWorkflow",
    "CopyNumberSegmentRelatesToCase",
    "CopyNumberVariationWorkflowPerformedOnCopyNumberSegment",
    "CopyNumberVariationWorkflowRelatesToCase",
    "DataFormat",
    "DataRelease",
    "DataSubtype",
    "DataType",
    "DataReleaseDescribesRoot",
    "DataReleaseRelatesToCase",
    "DataSubtypeMemberOfDataType",
    "Demographic",
    "DemographicDescribesCase",
    "DemographicRelatesToCase",
    "Diagnosis",
    "DiagnosisDescribesCase",
    "DiagnosisRelatesToCase",
    "ExperimentMetadata",
    "ExperimentalStrategy",
    "ExperimentMetadataDerivedFromFile",
    "ExperimentMetadataDerivedFromReadGroup",
    "ExperimentMetadataRelatesToCase",
    "Exposure",
    "ExposureDescribesCase",
    "ExposureRelatesToCase",
    "ExpressionAnalysisWorkflow",
    "ExpressionAnalysisWorkflowPerformedOnGeneExpression",
    "ExpressionAnalysisWorkflowRelatesToCase",
    "FamilyHistory",
    "FamilyHistoryDescribesCase",
    "FamilyHistoryRelatesToCase",
    "File",
    "FileDataFromAliquot",
    "FileDataFromAnalyte",
    "FileDataFromCase",
    "FileDataFromFile",
    "FileDataFromPortion",
    "FileDataFromSample",
    "FileDataFromSlide",
    "FileDescribesCase",
    "FileGeneratedFromPlatform",
    "FileMemberOfArchive",
    "FileMemberOfDataFormat",
    "FileMemberOfDataSubtype",
    "FileMemberOfExperimentalStrategy",
    "FileMemeberOfTag",
    "FileRelatedToFile",
    "FileRelatesToCase",
    "FileSubmittedByCenter",
    "FilteredCopyNumberSegment",
    "FilteredCopyNumberSegmentDataFromCopyNumberLiftoverWorkflow",
    "FilteredCopyNumberSegmentRelatesToCase",
    "FollowUp",
    "FollowUpDescribesCase",
    "FollowUpDescribesDiagnosis",
    "FollowUpRelatesToCase",
    "GeneExpression",
    "GeneExpressionDataFromRnaExpressionWorkflow",
    "GeneExpressionRelatesToCase",
    "GenomicProfileHarmonizationWorkflow",
    "GenomicProfileHarmonizationWorkflowPerformedOnSubmittedGenomicProfile",
    "GenomicProfileHarmonizationWorkflowRelatesToCase",
    "GermlineMutationCallingWorkflow",
    "GermlineMutationCallingWorkflowPerformedOnAlignedReads",
    "GermlineMutationCallingWorkflowPerformedOnSubmittedGenotypingArray",
    "GermlineMutationCallingWorkflowRelatesToCase",
    "MaskedMethylationArray",
    "MaskedSomaticMutation",
    "MaskedMethylationArrayDataFromMethylationArrayHarmonizationWorkflow",
    "MaskedMethylationArrayRelatesToCase",
    "MaskedSomaticMutationDataFromGenomicProfileHarmonizationWorkflow",
    "MaskedSomaticMutationDataFromSomaticAggregationWorkflow",
    "MaskedSomaticMutationDerivedFromProject",
    "MaskedSomaticMutationRelatesToCase",
    "MethylationArrayHarmonizationWorkflow",
    "MethylationBetaValue",
    "MethylationLiftoverWorkflow",
    "MethylationArrayHarmonizationWorkflowPerformedOnRawMethylationArray",
    "MethylationArrayHarmonizationWorkflowRelatesToCase",
    "MethylationBetaValueDataFromMethylationArrayHarmonizationWorkflow",
    "MethylationBetaValueDataFromMethylationLiftoverWorkflow",
    "MethylationBetaValueRelatesToCase",
    "MethylationLiftoverWorkflowPerformedOnSubmittedMethylationBetaValue",
    "MethylationLiftoverWorkflowRelatesToCase",
    "MirnaExpression",
    "MirnaExpressionWorkflow",
    "MirnaExpressionDataFromMirnaExpressionWorkflow",
    "MirnaExpressionRelatesToCase",
    "MirnaExpressionWorkflowPerformedOnAlignedReads",
    "MirnaExpressionWorkflowRelatesToCase",
    "MolecularTest",
    "MolecularTestPerformedAtFollowUp",
    "MolecularTestRelatedToDiagnosis",
    "MolecularTestRelatedToSlide",
    "MolecularTestRelatesToCase",
    "OtherClinicalAttribute",
    "OtherClinicalAttributeDescribesCase",
    "OtherClinicalAttributeDescribesFollowUp",
    "OtherClinicalAttributeRelatesToCase",
    "PathologyDetail",
    "PathologyReport",
    "PathologyDetailDescribesDiagnosis",
    "PathologyDetailRelatesToCase",
    "PathologyReportDerivedFromSample",
    "PathologyReportRelatesToCase",
    "Platform",
    "Portion",
    "PortionDerivedFromSample",
    "PortionRelatesToCase",
    "PortionShippedToCenter",
    "Program",
    "Project",
    "ProjectMemberOfProgram",
    "ProteinExpression",
    "ProteinExpressionDerivedFromPortion",
    "ProteinExpressionDerivedFromSample",
    "ProteinExpressionRelatesToCase",
    "Publication",
    "PublicationRefersToFile",
    "RawMethylationArray",
    "RawMethylationArrayDataFromAliquot",
    "RawMethylationArrayRelatesToCase",
    "ReadGroup",
    "ReadGroupQc",
    "ReadGroupDerivedFromAliquot",
    "ReadGroupQcDataFromSubmittedAlignedReads",
    "ReadGroupQcDataFromSubmittedUnalignedReads",
    "ReadGroupQcGeneratedFromReadGroup",
    "ReadGroupQcRelatesToCase",
    "ReadGroupRelatesToCase",
    "RnaExpressionWorkflow",
    "RnaExpressionWorkflowPerformedOnAlignedReads",
    "RnaExpressionWorkflowPerformedOnSubmittedAlignedReads",
    "RnaExpressionWorkflowPerformedOnSubmittedUnalignedReads",
    "RnaExpressionWorkflowRelatesToCase",
    "Root",
    "RootRelatesToCase",
    "RunMetadata",
    "RunMetadataDerivedFromFile",
    "RunMetadataDerivedFromReadGroup",
    "RunMetadataRelatesToCase",
    "Sample",
    "SampleDerivedFromCase",
    "SampleDerivedFromSample",
    "SampleProcessedAtTissueSourceSite",
    "SampleRelatedToDiagnosis",
    "SampleRelatesToCase",
    "SecondaryExpressionAnalysis",
    "SecondaryExpressionAnalysisDataFromExpressionAnalysisWorkflow",
    "SecondaryExpressionAnalysisRelatesToCase",
    "SimpleGermlineVariation",
    "SimpleSomaticMutation",
    "SimpleGermlineVariationDataFromGermlineMutationCallingWorkflow",
    "SimpleGermlineVariationRelatesToCase",
    "SimpleSomaticMutationDataFromGenomicProfileHarmonizationWorkflow",
    "SimpleSomaticMutationDataFromSomaticMutationCallingWorkflow",
    "SimpleSomaticMutationRelatesToCase",
    "Slide",
    "SlideImage",
    "SlideDerivedFromPortion",
    "SlideDerivedFromSample",
    "SlideImageDataFromSlide",
    "SlideImageRelatesToCase",
    "SlideRelatesToCase",
    "SomaticAggregationWorkflow",
    "SomaticAnnotationWorkflow",
    "SomaticCopyNumberWorkflow",
    "SomaticMutationCallingWorkflow",
    "SomaticMutationIndex",
    "SomaticAggregationWorkflowPerformedOnAnnotatedSomaticMutation",
    "SomaticAggregationWorkflowPerformedOnSimpleSomaticMutation",
    "SomaticAggregationWorkflowRelatesToCase",
    "SomaticAnnotationWorkflowPerformedOnSimpleSomaticMutation",
    "SomaticAnnotationWorkflowRelatesToCase",
    "SomaticCopyNumberWorkflowPerformedOnAlignedReads",
    "SomaticCopyNumberWorkflowPerformedOnSubmittedGenotypingArray",
    "SomaticCopyNumberWorkflowRelatesToCase",
    "SomaticMutationCallingWorkflowPerformedOnAlignedReads",
    "SomaticMutationCallingWorkflowRelatesToCase",
    "SomaticMutationIndexDerivedFromAnnotatedSomaticMutation",
    "SomaticMutationIndexDerivedFromSimpleSomaticMutation",
    "SomaticMutationIndexDerivedFromStructuralVariation",
    "SomaticMutationIndexRelatesToCase",
    "StructuralVariantCallingWorkflow",
    "StructuralVariation",
    "StructuralVariantCallingWorkflowPerformedOnAlignedReads",
    "StructuralVariantCallingWorkflowRelatesToCase",
    "StructuralVariationDataFromGenomicProfileHarmonizationWorkflow",
    "StructuralVariationDataFromStructuralVariantCallingWorkflow",
    "StructuralVariationRelatesToCase",
    "SubmittedAlignedReads",
    "SubmittedGenomicProfile",
    "SubmittedGenotypingArray",
    "SubmittedMethylationBetaValue",
    "SubmittedTangentCopyNumber",
    "SubmittedUnalignedReads",
    "SubmittedAlignedReadsDataFromReadGroup",
    "SubmittedAlignedReadsRelatesToCase",
    "SubmittedGenomicProfileDataFromReadGroup",
    "SubmittedGenomicProfileRelatesToCase",
    "SubmittedGenotypingArrayDerivedFromAliquot",
    "SubmittedGenotypingArrayRelatesToCase",
    "SubmittedMethylationBetaValueDerivedFromAliquot",
    "SubmittedMethylationBetaValueRelatesToCase",
    "SubmittedTangentCopyNumberDerivedFromAliquot",
    "SubmittedTangentCopyNumberRelatesToCase",
    "SubmittedUnalignedReadsDataFromReadGroup",
    "SubmittedUnalignedReadsRelatesToCase",
    "Tag",
    "TissueSourceSite",
    "Treatment",
    "TreatmentDescribesDiagnosis",
    "TreatmentRelatesToCase",
]


for __type in __all__:
    cls = sys.modules.get(__name__).__dict__.get(__type)
    cls.post_process()

__all__.append("Node")
__all__.append("Edge")

from sqlalchemy import orm

orm.configure_mappers()
